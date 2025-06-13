import httpx, asyncio, time
from typing import Optional
from .models import (
    MCPDocumentListResponse,
    MCPDocument,
    MCPUpdateIn,
)
from .cache import cached_ttl
from .config import settings

BASE = "https://readwise.io/api/v3"

class Reader:
    class RateLimited(Exception):
        def __init__(self, retry_after: int): self.retry_after = retry_after

    def __init__(self, token: str):
        self.h = {"Authorization": f"Token {token}"}
        self.client = httpx.AsyncClient(timeout=30.0)

    async def _get(self, url: str, params=None):
        r = await self.client.get(url, headers=self.h, params=params)
        if r.status_code == 429:
            raise Reader.RateLimited(int(r.headers.get("Retry-After", "60")))
        r.raise_for_status()
        return r.json()

    async def _patch(self, url: str, json):
        r = await self.client.patch(url, headers=self.h, json=json)
        r.raise_for_status()
        return r.json()

    # ---------- PUBLIC -----------
    @cached_ttl(ttl=settings.CACHE_TTL_S)
    async def list_documents(
        self,
        location: Optional[str],
        updated_after: Optional[str],
        with_html: bool,
        page_cursor: Optional[str],
    ) -> MCPDocumentListResponse:
        params = {}
        if location: params["location"] = location
        if updated_after: params["updatedAfter"] = updated_after
        if page_cursor: params["pageCursor"] = page_cursor
        if with_html: params["withHtmlContent"] = "true"
        data = await self._get(f"{BASE}/list/", params)
        return MCPDocumentListResponse.model_validate(data)

    async def get_document(self, doc_id: str, with_html: bool = False) -> Optional[MCPDocument]:
        params = {"id": doc_id}
        if with_html:
            params["withHtmlContent"] = "true"
        data = await self._get(f"{BASE}/list/", params)
        if data["results"]:
            return MCPDocument.model_validate(data["results"][0])
        return None

    async def update_document(self, doc_id: str, payload: MCPUpdateIn) -> MCPDocument:
        await self._patch(f"{BASE}/update/{doc_id}/", payload.model_dump(exclude_none=True))
        self.list_documents.cache_clear()
        # Fetch and return the updated document
        doc = await self.get_document(doc_id)
        if not doc:
            raise Exception("Document updated but not found")
        return doc
