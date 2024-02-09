from models import *
from utilities import *
from constants import *


async def do_search(search_request: SearchRequest):
    qdrant_client = get_qdrant_client()
    openai_client = get_openai_client()
    embed = await openai_client.embeddings.create(input=search_request.query, model=OPENAI_EMBEDDING_MODEL)
    vector = embed.data[0].embedding
    results = await qdrant_client.search(search_request.collection,
                                         query_vector=vector,
                                         limit=search_request.limit,
                                         with_payload=["url", "body"])
    search_links = []
    for i, result in enumerate(results):
        search_links.append(
            {
                "rank": f"{i + 1}",
                "url": result.payload["url"],
                "score": result.score
            }
        )
    return search_links
