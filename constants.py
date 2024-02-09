from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Access environment variables
API_KEY_HEADER_NAME = os.getenv('API_KEY_HEADER_NAME')
API_KEY = os.getenv('API_KEY')

QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ORGANIZATION = os.getenv('OPENAI_ORGANIZATION')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')
OPENAI_EMBEDDING_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL')
VECTOR_SIZE = int(os.getenv('VECTOR_SIZE', 1536))  # Provides a default value if not set

GRAPHQL_URL = os.getenv('GRAPHQL_URL')
GRAPHQL_ADMIN_SECRET = os.getenv('GRAPHQL_ADMIN_SECRET')

GRAPHQL_HEADERS = {
    "Content-Type": "application/json",
    "x-hasura-admin-secret": GRAPHQL_ADMIN_SECRET
}

GET_THREAD_GRAPHQL = """query ThreadMessages($thread_id: String!) {
  thread_by_pk(thread_id: $thread_id) {
    thread_id
    title
    collection
    messages(order_by: {created_at: asc}) {
      content
      from_bot
      first_message
      mentions_bot
    }
  }
}
"""

INSERT_MESSAGE_GRAPHQL = """mutation InsertMessage($object: message_insert_input!) {
  insert_message_one(object: $object) {
    thread_id
    message_id
    content
    sources
    from_bot
    first_message
    mentions_bot
    created_at
    updated_at
    processed
  }
}"""
