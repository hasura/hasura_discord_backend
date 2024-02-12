from upload import upload_docs

if __name__ == "__main__":
    API_URL = "http://localhost:8100"
    API_KEY = "secret"
    docs_JSON = "files/zapier_docs.json"
    collection = "zapier"
    tags = ["Docs zapier"]
    upload_docs(API_URL, API_KEY, docs_JSON, collection, tags)