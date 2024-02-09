import json
import requests

API_URL = "http://localhost:8100"
API_KEY = "secret"
v2_docs_JSON = "files/v2_docs.json"


def upload_v2_docs():
    with open(v2_docs_JSON, "r") as f:
        data = json.load(f)
    i = 0
    doc_set = set()
    print(len(data))
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
                    "collection": "docs_v2",
                    "document":
                        {
                            "body": v,
                            "source": "Docs V2",
                            "tags": [
                                "Docs V2"
                            ],
                            "url": k,
                            "uid": i
                        }
                }
            )
        )
        if response.status_code == 200:
            i += response.json()


if __name__ == "__main__":
    upload_v2_docs()
