# Every project has dragons. here they lie. 🐉
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup, NavigableString, Tag
import json
import os
import random

VISITED_LIS = set()
INDENT_DICT = dict()


def get_driver():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    return driver


driver = get_driver()


def ensure_directory_exists(path):
    os.makedirs(path, exist_ok=True)


def is_url_valid(url, pattern):
    return re.match(pattern, url) is not None


def process_element(element, indent_level=0, link_root="", docs_root="", list_prefix="-"):
    if isinstance(element, NavigableString):
        return element.strip()
    elif isinstance(element, Tag):
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            header_level = int(element.name[1])  # Extracting the header level
            return '#' * header_level + ' ' + element.get_text().strip()
        elif element.name == 'p':
            paragraph_content = ''
            for child in element.children:
                if isinstance(child, NavigableString):
                    paragraph_content += child.strip()
                elif child.name == 'br':
                    paragraph_content += '\n'
                elif child.name == 'code':  # Inline code within paragraph
                    code_text = child.get_text(separator=" ")
                    paragraph_content += ' `' + code_text + '` '
                else:
                    child_text = process_element(child, indent_level, link_root, docs_root)
                    if child_text:
                        paragraph_content += child_text
            return paragraph_content
        elif element.name in ['ul', 'ol']:
            markdown = ''
            for i, li in enumerate(element.find_all(['li'], recursive=True)):
                e = process_element(li, indent_level, link_root, docs_root,
                                    list_prefix="-" if element.name == "ul" else f"{i + 1}.")
                if e is not None and li.parent.parent.name != "li":
                    markdown += e + '\n'
                elif e is not None:
                    indent_level = 0
                    if e not in VISITED_LIS:
                        VISITED_LIS.add(e.strip())
                        INDENT_DICT[e] = indent_level + 1
                        markdown += "\n" + e + "\n"
            return markdown
        elif element.name == 'li':
            item_content = ''
            for child in element.children:
                if child.name == 'code':
                    # Inline code within list item
                    code_text = child.get_text(separator=" ", strip=True)
                    item_content += ' `' + code_text + '` '
                elif isinstance(child, (NavigableString, Tag)):
                    child_text = process_element(child, indent_level + 1, link_root, docs_root)
                    if child_text:
                        item_content += child_text
                else:
                    return None
            indent = '    ' * indent_level
            return f'{indent}{list_prefix} {item_content.strip()}'
        elif element.name == 'a':
            text = element.get_text()
            href = element.get('href')
            # Check if the URL is valid according to the specified pattern
            if not is_url_valid(href, "https?://.+"):
                if href.startswith("#"):
                    href = link_root.rstrip('/') + '/' + href.lstrip('/')
                elif href.startswith("/"):
                    href = docs_root.rstrip("/") + "/" + href.lstrip("/")
            return f'[ {text} ]({href})'
        elif element.name == 'code':
            if element.parent.name in ["ul", "li", "td", "th", "a"]:
                return None
            code_contents = []
            for child in element.children:
                child_text = process_element(child, indent_level, link_root, docs_root)
                if child_text:
                    code_contents.append(child_text)
            if len(code_contents) == 1:
                return '`' + code_contents[0] + '`'
            return '```\n' + "\n".join(code_contents) + '\n```'
        elif element.name == 'span':
            return element.get_text(separator=" ")
        elif element.name == 'strong':
            return ' **' + element.get_text(separator=" ") + '** '
        elif element.name == "em":
            return " *" + element.get_text() + "* "
        elif element.name == "img":
            href = element.get('src', '')
            text = element.get("alt", "")
            if href.startswith("data:image"):
                return None  # or you can return a placeholder text like "Image: [Embedded Image]"
            else:
                if len(href) > 0 and len(text) > 0:
                    if not is_url_valid(href, "https?://.+"):
                        if href.startswith("#"):
                            href = link_root.rstrip('/') + '/' + href.lstrip('/')
                        elif href.startswith("/"):
                            href = docs_root.rstrip("/") + "/" + href.lstrip("/")
                    return f'Image: [ {text} ]({href})'
        elif element.name == 'iframe':
            iframe_src = element.get('src', '')
            if iframe_src.startswith("https://www.youtube.com/"):
                return f"Embedded content: [ View content ]({iframe_src})"
            else:
                return None
        elif element.name == 'table':
            markdown = ''
            for child in element.children:
                if child.name in ['thead', 'tbody']:
                    for row in child.find_all('tr'):
                        row_content = '|'
                        for cell in row.find_all(['th', 'td']):
                            print(cell)
                            cell_content = process_element(cell, indent_level + 1, link_root, docs_root)
                            row_content += f' {cell_content} |'
                        markdown += row_content + '\n'
                        if child.name == 'thead':  # After header row, add the separator
                            markdown += '|' + '---|' * len(row.find_all(['th', 'td'])) + '\n'
            return markdown
        elif element.name == "td":
            paragraph_content = ''
            for child in element.children:
                if isinstance(child, NavigableString):
                    paragraph_content += child.strip()
                elif child.name == 'br':
                    paragraph_content += '\n'
                elif child.name == 'code':  # Inline code within paragraph
                    code_text = child.get_text(separator=" ")
                    paragraph_content += ' `' + code_text + '` '
                else:
                    child_text = process_element(child, indent_level, link_root, docs_root)
                    if child_text:
                        paragraph_content += child_text
            return paragraph_content
        elif element.name == "th":
            return element.get_text()
    return None


def scrape_content(soup, link_root, docs_root):
    content = []
    found_main_header = False
    for child in soup.find_all(['h1',
                                'h2',
                                'h3',
                                'h4',
                                'h5',
                                'h6',
                                'p',
                                'ul',
                                'ol', 'code', "span", "iframe", "img", "table"]):
        if child.name == 'h1':
            found_main_header = True
        if found_main_header:
            if child.name == "span":
                class_list = child.get('class', [])  # Safely get the class list
                for class_name in class_list:
                    if class_name.startswith("admonitionIcon"):
                        child_content = child.parent.get_text()
                        content.append(child_content)
                        break  # Break the loop once the condition is met
                continue
            if child.name == "code" and child.parent.name == "p":
                continue
            child_content = process_element(child, 0, link_root=link_root, docs_root=docs_root)
            if child_content:
                content.append(child_content)
    return "\n\n".join(content)


def get_links(soup, root):
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        href = root + href
        if is_url_valid(href, r'https?://.+'):
            links.append(href)
    return links


def scrape_page(url, docs_root, recurse=0):
    global driver
    try:
        print(f"Processing URL: {url}")
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = scrape_content(soup, url, docs_root)
        links = get_links(soup, docs_root)
        print(links)
        return content, links
    except Exception as e:
        print("EXCEPTION")
        time.sleep(recurse + 1)
        if recurse > 3:
            return "", []
        driver = get_driver()
        return scrape_page(url, docs_root, recurse=recurse + 1)


def scrape_docs(root_url, root_file, docs_root, doc_dict, dev=True, wait_time=1):
    document_text = ""
    urls_to_visit = [root_url]
    visited_urls = set()

    while urls_to_visit:
        current_url = urls_to_visit.pop(0)
        if current_url in visited_urls or not current_url.startswith(root_url):
            continue

        main_page_content, links = scrape_page(current_url, docs_root)
        visited_urls.add(current_url)

        if main_page_content:
            doc_dict[current_url] = main_page_content
            # Prepare the file path
            file_path = f"{root_file}/{current_url.replace(root_url, '').strip('/')}.md"
            # Ensure the directory exists
            ensure_directory_exists(os.path.dirname(file_path))
            # Write the file
            with open(file_path, "w") as _f:
                _f.write(main_page_content)

        for link in links:
            urls_to_visit.append(link)

            # if link not in visited_urls and link not in urls_to_visit and link.startswith(root_url):
            # urls_to_visit.append(link)
            # if link.startswith("https://hasura.io/docs/3.0/data-domain-modeling/"):
            #     print(link)
            #     urls_to_visit.append(link)

        if dev:
            print(urls_to_visit)
            # print(main_page_content)
            choice = input("Continue to next link? (yes/no): ").strip().lower()
            if choice == 'no':
                break

        # if not urls_to_visit or "https://hasura.github.io/ndc-spec/reference/json-schema.html" == current_url:
        #     break

        time.sleep(0.01)

    driver.quit()
    return document_text


# Run the scraper and save the output to a file
docs = {}
root_url = "https://hasura.io/docs/3.0/"
root_file = "files/hasura3/"
link_root = "https://hasura.io"
markdown_document = scrape_docs(root_url,
                                root_file,
                                link_root,
                                docs,
                                dev=False,
                                wait_time=4)

with open(f"{root_file}/docs.json", "w") as f:
    json.dump(docs, f)
