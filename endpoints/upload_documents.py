from models import *
from utilities import *
from constants import *
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from qdrant_client.http.exceptions import UnexpectedResponse


async def do_upload_documents(documents: UploadDocumentsRequest):
    collection = documents.collection
    qdrant_client = get_qdrant_client()
    openai_client = get_openai_client()
    try:
        await qdrant_client.get_collection(collection_name=collection)
    except UnexpectedResponse:
        await qdrant_client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )
    doc = documents.document
    chunks = chunk_document(doc.body)
    offset = 0
    initial_id = doc.uid
    for c in chunks:
        embed = await openai_client.embeddings.create(input=c, model=OPENAI_EMBEDDING_MODEL)
        vector = embed.data[0].embedding
        parent = None
        if offset > 0:
            parent = initial_id + offset - 1
        await qdrant_client.upload_points(collection_name=collection,
                                          points=[PointStruct(
                                              id=initial_id + offset,
                                              vector=vector,
                                              payload={
                                                  "source": doc.source,
                                                  "parent": parent,
                                                  "tags": doc.tags,
                                                  "url": doc.url,
                                                  "body": c
                                              }
                                          )])
        offset += 1
    return offset
