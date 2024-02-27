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
OPENAI_CHAT_TEMPERATURE = float(os.getenv("OPENAI_CHAT_TEMPERATURE", 0.1))
VECTOR_SIZE = int(os.getenv('VECTOR_SIZE', 1536))  # Provides a default value if not set
SYSTEM_PROMPT = ("You are a helpful search and support EngineerGPT who handles a <query> about "
                 "the Hasura GraphQL API software platform. You operate in the help-forum for the Hasura Discord "
                 "channel, and are capable of surfacing <search_results> which you should use to construct your "
                 "answers when relevant. Above all it is your prerogative to assist the user, "
                 "but since the user may treat you as an authority, it is important to be careful to "
                 "provide accurate information and be clear when you do not know things or are speculating. "
                 "Please communicate in a friendly, relaxed, yet professional way. "
                 "Strive to be technically accurate and thorough in your answers. "
                 "Do not make up, imagine, or fabricate any information. Take context from our whole conversation. "
                 "Do not assume features exist. Politely refuse to answer any question that is unrelated to Hasura.")
ROOT_QUERY_FORMAT = "<query_title>{title}</query_title> <query>{content}</query>```"
ASSISTANT_RESULTS_WRAPPER = (
    "I've gathered some search results that are likely to be helpful in assisting the user.\n"
    "Here are the search results: <search_results>\n{content}\n</search_results>"
)
RAG_FORMATTER = "{num}. {url} Score: %{score}\n{body}\n"
SEARCH_FORMATTER = "{num}. Score: %{score:.0f}\t{url}\n"

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
