import json
import requests

API_URL = "http://localhost:8100"
API_KEY = "secret"
docs_JSON = "files/v3_docs.json"
collection = "docs_v3"
tags = ["Docs V3"]


def upload_v3_docs():
    with open(docs_JSON, "r") as f:
        data = json.load(f)
    i = 0
    doc_set = set()
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


if __name__ == "__main__":
    upload_v3_docs()
