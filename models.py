from pydantic import BaseModel
from typing import Optional, List, Literal, Dict, Any

DocumentSources = Literal[
    'Docs V2',
    'Docs V3',
    'Discord',
    'ZenDesk',
    'StackOverflow',
    'Reddit',
    'Slack',
    "Docs fly.io",
    "Docs Turso",
    "Docs Ionic",
    "Docs Clickhouse"
]


class CreateDocumentForm(BaseModel):
    uid: int
    body: str
    source: DocumentSources
    url: str
    tags: List[str] = []


class UploadDocumentsRequest(BaseModel):
    collection: str
    document: CreateDocumentForm


class Document(BaseModel):
    uid: int
    chunk: int
    body: str
    source: DocumentSources
    tags: Optional[List[str]] = None
    url: Optional[str] = None
    size: int


class SearchRequest(BaseModel):
    collection: str
    query: str
    limit: int = 10
    positive: List[int] = []
    negative: List[int] = []


class EventBodyTraceContext(BaseModel):
    trace_id: str | None = None
    span_id: str | None = None


class EventBodyData(BaseModel):
    old: Dict[str, Any] | None = None
    new: Dict[str, Any] | None = None


class EventBody(BaseModel):
    op: str | None = None
    data: EventBodyData | None = None
    trace_context: EventBodyTraceContext | None = None


class EventDeliveryInfo(BaseModel):
    max_retries: int | None = None
    current_retry: int | None = None


class EventTrigger(BaseModel):
    name: str | None = None


class Event(BaseModel):
    event: EventBody | None = None
    created_at: str | None = None
    id: str | None = None
    delivery_info: EventDeliveryInfo | None = None
    trigger: EventTrigger | None = None
    table: Dict[str, str] | None = None
