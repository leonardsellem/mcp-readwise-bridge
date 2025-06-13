# MCP Readwise Bridge

A FastAPI MCP server that exposes your Readwise Reader library to MCP-compatible clients (Claude, VS Code, etc).

## Features
- List, retrieve, and update your Readwise Reader documents via a simple HTTP API
- Supports pagination, filtering, and HTML content retrieval
- Handles Readwise rate limits and authentication
- In-memory caching for efficiency

## Usage

1. **Clone and install**
   ```bash
   git clone https://github.com/leonardsellem/mcp-readwise-bridge.git
   cd mcp-readwise-bridge
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure**
   - Copy `.env.example` to `.env` and set your Readwise token:
     ```env
     READWISE_TOKEN=rw_live_xxx
     CACHE_TTL_S=300
     ```

3. **Run**
   ```bash
   uvicorn mcp_reader_bridge.app:api --reload --port 5678
   # Swagger UI: http://localhost:5678/docs
   ```

## Endpoints
| Endpoint | Method | Description |
|---|---|---|
| /list_documents | GET | List documents (filter, paginate, withContent) |
| /get_document/{id} | GET | Retrieve a single document |
| /update_document/{id} | PATCH | Update document fields |

## License
MIT
