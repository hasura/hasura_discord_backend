from upload import upload_docs

if __name__ == "__main__":
    API_URL = "http://localhost:8100"
    API_KEY = "secret"
    docs_JSON = "files/turso_docs.json"
    collection = "turso"
    tags = ["Docs Turso"]
    upload_docs(API_URL, API_KEY, docs_JSON, collection, tags)
