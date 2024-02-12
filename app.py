from fastapi import FastAPI, Depends, Body, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from endpoints.new_message_event import do_new_message_event
from endpoints.search import do_search
from endpoints.upload_documents import do_upload_documents
from models import *
from constants import *

# Initialize the FastAPI app
app = FastAPI()

api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME)


# Dependency for API key authentication
async def get_api_key(header: str = Depends(api_key_header)):
    if header == API_KEY:
        return header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


# Add CORS middleware to allow cross-origin requests
# Customize the following parameters according to your needs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/upload_documents/", dependencies=[Depends(get_api_key)])
async def upload_document(documents: UploadDocumentsRequest):
    return await do_upload_documents(documents)


@app.post("/search/", dependencies=[Depends(get_api_key)])
async def search(search_request: SearchRequest):
    return await do_search(search_request)


@app.post("/new_message_event/", dependencies=[Depends(get_api_key)])
async def new_message_event(data: Event = Body(...)):
    return await do_new_message_event(data)


if __name__ == "__main__":
    uvicorn.run(app, port=os.getenv("PORT", 8080))
