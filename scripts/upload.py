import json
import requests


def upload_docs(API_URL, API_KEY, docs_JSON, collection, tags):
    with open(docs_JSON, "r") as f:
        data = json.load(f)
    i = 0
    doc_set = set()
    print(f"There are {len(data)} docs")
    for k, v in data.items():
        if v in doc_set:
            continue
        else:
            doc_set.add(v)
        response = requests.request(
            method="POST",
            url=f"{API_URL}/upload_documents/",
            headers={
                "X-API-KEY": API_KEY
            },
            data=json.dumps(
                {
                    "collection": collection,
                    "document":
                        {
                            "body": v,
                            "source": tags[0],
                            "tags": tags,
                            "url": k,
                            "uid": i
                        }
                }
            )
        )
        if response.status_code == 200:
            i += response.json()
