from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class MCPDocument(BaseModel):
    id: str
    url: str
    source_url: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    tags: Optional[Dict[str, str]] = None
    summary: Optional[str] = None
    updated_at: Optional[str] = None
    created_at: Optional[str] = None
    html_content: Optional[str] = None  # present only when requested
    # + any other fields you care about …

class MCPDocumentListResponse(BaseModel):
    count: int
    nextPageCursor: Optional[str] = None
    results: List[MCPDocument]

class MCPUpdateIn(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    summary: Optional[str] = None
    published_date: Optional[str] = None
    image_url: Optional[str] = None
    location: Optional[str] = Field(None, pattern="^(new|later|archive|feed)$")
    category: Optional[str] = None
