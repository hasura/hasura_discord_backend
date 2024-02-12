from models import *
from utilities import *
from constants import *
from uuid import uuid4


# TODO: Move strings to constants to make it easier to make this multi-lingual
async def do_new_message_event(data: Event):
    qdrant_client = get_qdrant_client()
    openai_client = get_openai_client()
    message_data = data.event.data.new
    if message_data["from_bot"]:
        return
    else:
        if message_data["first_message"] or message_data["mentions_bot"]:
            thread_data = await execute_graphql(GRAPHQL_URL,
                                                GET_THREAD_GRAPHQL,
                                                {"thread_id": message_data["thread_id"]},
                                                GRAPHQL_HEADERS)
            thread = thread_data.get("data", {}).get("thread_by_pk", None)
            if thread is None:
                return
            title = thread.get("title")
            collection = thread.get("collection")
            messages = [
                {"role": "system",
                 "content": SYSTEM_PROMPT
                 }
            ]
            vector_content = ""
            for i, message in enumerate(thread.get("messages")):
                if i == 0:
                    message["content"] = ROOT_QUERY_FORMAT.format(title=title, content=message["content"])
                new_message = {
                    "role": "assistant" if message_data["from_bot"] else "user",
                    "content": message["content"]
                }
                messages.append(new_message)
                vector_content += new_message["content"] + "\n"

            embed = await openai_client.embeddings.create(input=vector_content, model=OPENAI_EMBEDDING_MODEL)
            vector = embed.data[0].embedding
            results = await qdrant_client.search(collection,
                                                 query_vector=vector,
                                                 limit=5,
                                                 with_payload=["url", "body"])
            formatted_text = ""
            search_links = ""
            for i, result in enumerate(results):
                formatted_text += RAG_FORMATTER.format(num=i + 1,
                                                       url=result.payload["url"],
                                                       score=result.score,
                                                       body=result.payload["body"])
                search_links += SEARCH_FORMATTER.format(num=i + 1,
                                                        score=result.score,
                                                        url=result.payload["url"])
            result_text = ASSISTANT_RESULTS_WRAPPER.format(content=formatted_text)
            messages.append({
                "role": "assistant",
                "content": result_text
            })
            completion = await openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages
            )
            result = completion.choices[0].message.content
            # Add a message to the thread.
            variables = {
                "object": {
                    "thread_id": message_data["thread_id"],
                    "message_id": str(uuid4()),
                    "content": result,
                    "from_bot": True,
                    "first_message": False,
                    "mentions_bot": False,
                    "sources": search_links,
                    "processed": False
                }
            }
            await execute_graphql(GRAPHQL_URL,
                                  INSERT_MESSAGE_GRAPHQL,
                                  variables,
                                  GRAPHQL_HEADERS)
