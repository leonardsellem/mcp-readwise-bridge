from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from .config import settings
from .readwise import Reader
from .models import (
    MCPDocumentListResponse,
    MCPDocument,
    MCPUpdateIn,
)

api = FastAPI(
    title="Readwise-Reader MCP Bridge",
    version="1.0.0",
    description="Expose Readwise Reader as MCP-compatible tools.",
)

reader = Reader(settings.READWISE_TOKEN)


@api.get("/list_documents", response_model=MCPDocumentListResponse)
async def list_documents(
    location: Optional[str] = Query(None, pattern="^(new|later|shortlist|archive|feed)$"),
    updatedAfter: Optional[str] = None,
    withContent: bool = False,
    pageCursor: Optional[str] = None,
):
    try:
        return await reader.list_documents(
            location=location,
            updated_after=updatedAfter,
            with_html=withContent,
            page_cursor=pageCursor,
        )
    except Reader.RateLimited as rl:
        # Surface 429 to client with wait-time
        raise HTTPException(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limited ‑ retry after {rl.retry_after}s",
            headers={"Retry-After": str(rl.retry_after)},
        )


@api.get("/get_document/{doc_id}", response_model=MCPDocument)
async def get_document(doc_id: str, withContent: bool = False):
    doc = await reader.get_document(doc_id, with_html=withContent)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@api.patch("/update_document/{doc_id}", response_model=MCPDocument)
async def update_document(doc_id: str, payload: MCPUpdateIn):
    return await reader.update_document(doc_id, payload)
