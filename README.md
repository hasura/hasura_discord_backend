# Hasura Discord Backend

This repo has the code that runs the backend for the Hasura Discord project!

This is a very simple FastAPI.

There are also some scripts that might be useful in the `scripts` folder.

To run the code, first copy .env.example to a .env file.

Fill out the .env with the endpoints you'd like to have used.

The header the API requires the API-KEY be sent to for authentication:
`API_KEY_HEADER_NAME=X-API-KEY`

The API-KEY to use:
`API_KEY=secret`

The url of the Qdrant database:
`QDRANT_URL=http://localhost:6333`

The Qdrant API Key:
`QDRANT_API_KEY=secret`

The API key used to authenticate with OpenAI:
`OPENAI_API_KEY=key`

The OpenAI organization-ID:
`OPENAI_ORGANIZATION=org`

The model of GPT the bot should use:
`OPENAI_MODEL=gpt-4-turbo-preview`

The embedding model to use:
`OPENAI_EMBEDDING_MODEL=text-embedding-3-large`

The size of the vector for the embedding model:
`VECTOR_SIZE=3072`

The GraphQL url endpoint for GraphQL engine:
`GRAPHQL_URL=https://hasura-bots.hasura.app/v1/graphql`

The GraphQL Admin secret:
`GRAPHQL_ADMIN_SECRET=admin_secret`

Run the application via `python3 app.py`