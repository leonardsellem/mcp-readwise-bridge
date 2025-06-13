# MCP Readwise Bridge

A FastAPI MCP server that exposes your Readwise Reader library to MCP-compatible clients (Claude, VS Code, Cursor, Raycast, and more).

---

## Features
- List, retrieve, and update your Readwise Reader documents via a simple HTTP API
- Supports pagination, filtering, and HTML content retrieval
- Handles Readwise rate limits and authentication
- In-memory caching for efficiency
- Compatible with any client that supports the [MCP protocol](https://github.com/multi-client-protocol/mcp)

---

## Quickstart

### 1. Clone and Install

```bash
git clone https://github.com/leonardsellem/mcp-readwise-bridge.git
cd mcp-readwise-bridge
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure

Copy `.env.example` to `.env` and set your Readwise token:

```bash
cp .env.example .env
# Edit .env and set READWISE_TOKEN=rw_live_xxx (get your token from https://readwise.io/access_token)
```

### 3. Run the Server

```bash
uvicorn mcp_reader_bridge.app:api --reload --port 5678
```

- The server will be available at: [http://localhost:5678](http://localhost:5678)
- Swagger UI for testing: [http://localhost:5678/docs](http://localhost:5678/docs)

---

## 🚀 One-Click Install for IDEs (VS Code, Cursor, Raycast, Claude, etc.)

Paste the following block into your IDE’s MCP extension or “Add Server” dialog for instant setup:

```json
{
  "mcp": {
    "inputs": [
      {
        "type": "promptString",
        "id": "readwise_token",
        "description": "Readwise Access Token (get from https://readwise.io/access_token)",
        "password": true
      }
    ],
    "servers": {
      "readwise": {
        "command": "docker",
        "args": [
          "run",
          "-i",
          "--rm",
          "-e",
          "READWISE_TOKEN",
          "-p",
          "5678:5678",
          "ghcr.io/leonardsellem/mcp-readwise-bridge:latest"
        ],
        "env": {
          "READWISE_TOKEN": "${input:readwise_token}"
        }
      }
    }
  }
}
```

- This will prompt you for your Readwise token and launch the server in Docker.
- The server will be available at `http://localhost:5678` for your IDE or AI client.

---

## Connecting to Clients

### VS Code (with Claude, Cursor, or other MCP plugins)
1. **Install the MCP extension** (e.g., [Cursor MCP](https://github.com/multi-client-protocol/mcp), [Claude VS Code](https://www.anthropic.com/blog/claude-vscode), or your preferred MCP-compatible extension).
2. **Add a new MCP server** in the extension settings:
    - **Server URL:** `http://localhost:5678`
    - **(Optional) Name:** `Readwise MCP`
3. **Authenticate** if prompted (the server uses your `.env` token, no extra login needed).
4. **Use the extension’s UI** to browse, search, and update your Readwise documents directly from VS Code.

### Claude (Anthropic)
- In Claude’s “Connect Knowledge” or “Add Source” dialog, select “Custom MCP server” and enter `http://localhost:5678`.
- Claude will now be able to list, retrieve, and update your Readwise documents.

### Cursor
- Open Cursor’s command palette and search for “Connect MCP Server”.
- Enter `http://localhost:5678` as the endpoint.
- You can now use Cursor’s AI features with your Readwise library.

### Raycast
- Install the [Raycast MCP extension](https://raycast.com/extensions?search=mcp).
- Add a new MCP server with the URL `http://localhost:5678`.
- Raycast will now let you search and interact with your Readwise documents.

---

## Troubleshooting

- **401 Unauthorized:** Make sure your `READWISE_TOKEN` is correct and not expired.
- **429 Rate Limited:** The Readwise API has request limits. Wait a minute and try again.
- **Cannot connect:** Ensure the server is running and accessible at the port you specified.
- **Firewall/Network:** If connecting from another device, ensure your firewall allows incoming connections on the server port.

---

## Endpoints

| Endpoint                | Method | Description                                      |
|-------------------------|--------|--------------------------------------------------|
| /list_documents         | GET    | List documents (filter, paginate, withContent)   |
| /get_document/{id}      | GET    | Retrieve a single document                       |
| /update_document/{id}   | PATCH  | Update document fields                           |

---

## FAQ

**Q: Is my Readwise data safe?**  
A: Yes. Your token is stored locally in `.env` and never shared with clients. The server only proxies requests.

**Q: Can I run this on a remote server?**  
A: Yes, but you may need to set up HTTPS and firewall rules for security.

**Q: Can I use this with other MCP clients?**  
A: Yes! Any client that supports the MCP protocol can connect.

---

## License

MIT

---

## Links

- [Readwise Reader API Docs](https://readwise.io/reader_api)
- [Multi-Client Protocol (MCP)](https://github.com/multi-client-protocol/mcp)
- [Claude VS Code](https://www.anthropic.com/blog/claude-vscode)
- [Cursor](https://www.cursor.so/)
- [Raycast](https://raycast.com/)
