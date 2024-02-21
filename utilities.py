from constants import *
from qdrant_client.async_qdrant_client import AsyncQdrantClient
from openai import AsyncOpenAI
import tiktoken
from typing import List, Any
import aiohttp


# TODO: Create a client pool
def get_qdrant_client() -> AsyncQdrantClient:
    return AsyncQdrantClient(url=QDRANT_URL,
                             api_key=QDRANT_API_KEY,
                             timeout=60)


def get_openai_client() -> AsyncOpenAI:
    return AsyncOpenAI(api_key=OPENAI_API_KEY,
                       organization=OPENAI_ORGANIZATION
                       )


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def chunk_document(body: str, max_tokens: int = 8100, encoding_name: str = "cl100k_base") -> List[str]:
    # Initialize the tokenizer with the specified encoding
    encoding = tiktoken.get_encoding(encoding_name)

    # Encode the entire document body
    tokens = encoding.encode(body)

    # Split the tokens into chunks
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        # Decode the chunk back into a string
        chunk = encoding.decode(tokens[i:i + max_tokens])
        chunks.append(chunk)

    return chunks


async def execute_graphql(url, query, variables, headers) -> Any:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={'query': query, 'variables': variables}, headers=headers) as response:
            if response.status == 200:
                return await response.json()  # Process the JSON response
            else:
                return False
