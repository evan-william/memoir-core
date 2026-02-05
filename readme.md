# Memoir-Core

<div align="center">

![Claude](https://img.shields.io/badge/Claude-191919?style=for-the-badge&logo=anthropic&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Long-term Memory Database for Claude AI**

A lightweight, persistent memory solution that enables Claude to remember information across conversations.

[Features](#features) • [Quick Start](#quick-start) • [Installation](#installation) • [Documentation](#claude-integration) • [Contributing](#contributing)

</div>

---

## Overview

Memoir-Core provides Claude with persistent memory capabilities through a lightweight SQLite database and pure Streamlit interface. Store user preferences, important facts, and conversational context that persists across different chat sessions.

### Key Features

- **Persistent Storage** - SQLite-backed memory that survives session restarts
- **Full-Text Search** - Search across both keys and content with case-insensitive matching
- **Web Interface** - Streamlit-based UI for manual memory management
- **RESTful API** - Query parameter-based endpoints for seamless Claude integration
- **Zero Configuration** - Deploy to Streamlit Cloud without additional setup
- **Minimal Dependencies** - Only Streamlit and Pandas required

## Architecture

```
┌─────────────────────┐
│   Claude.ai         │
│   Custom Tools API  │
└──────────┬──────────┘
           │
           │ HTTPS GET
           │ Query Parameters
           ▼
┌─────────────────────┐
│  Streamlit App      │
│  ┌───────────────┐  │
│  │ Query Handler │  │
│  │ Web Interface │  │
│  │ API Endpoints │  │
│  └───────────────┘  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  SQLite Database    │
│  memoir_core.db     │
└─────────────────────┘
```

## Quick Start

### Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/memoir-core.git
cd memoir-core

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

Access the application at `http://localhost:8501`

### Deployment

#### Streamlit Cloud

1. **Prepare Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/memoir-core.git
   git push -u origin main
   ```

2. **Deploy**
   - Navigate to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click **New app**
   - Select repository: `memoir-core`
   - Main file path: `app.py`
   - Click **Deploy**

3. **Note Deployment URL**
   ```
   https://your-app-name.streamlit.app
   ```

## API Reference

### Endpoints

| Endpoint | Method | Parameters | Description |
|----------|--------|------------|-------------|
| `/?api=health` | GET | None | Health check |
| `/?api=store_memory` | GET | `key`, `content` | Store/update memory |
| `/?api=search_memory` | GET | `query` | Search memories |
| `/?api=get_memory` | GET | `key` | Retrieve specific memory |

### Testing API

```bash
# Health check
curl "https://your-app-name.streamlit.app/?api=health"

# Store memory
curl "https://your-app-name.streamlit.app/?api=store_memory&key=user_name&content=John%20Doe"

# Search memories
curl "https://your-app-name.streamlit.app/?api=search_memory&query=john"

# Get specific memory
curl "https://your-app-name.streamlit.app/?api=get_memory&key=user_name"
```

## Claude Integration

### Setup Custom Tools

1. **Enable Custom Tools**
   - Open [claude.ai](https://claude.ai)
   - Navigate to Settings → Feature Preview
   - Enable **Custom Tools**

2. **Add store_memory Tool**

   **Tool Name:** `store_memory`

   **Description:**
   ```
   Store important information to long-term memory database. Use this to remember user preferences, facts, or any information that should persist across conversations.
   ```

   **Input Schema:**
   ```json
   {
     "type": "object",
     "properties": {
       "key": {
         "type": "string",
         "description": "Unique identifier for this memory (e.g., 'user_name', 'favorite_food', 'project_deadline')"
       },
       "content": {
         "type": "string",
         "description": "The information to store in memory"
       }
     },
     "required": ["key", "content"]
   }
   ```

   **API Configuration:**
   - Method: `GET`
   - URL: `https://your-app-name.streamlit.app/?api=store_memory&key={{key}}&content={{content}}`

3. **Add search_memory Tool**

   **Tool Name:** `search_memory`

   **Description:**
   ```
   Search for information in the long-term memory database. Use this to recall previously stored information.
   ```

   **Input Schema:**
   ```json
   {
     "type": "object",
     "properties": {
       "query": {
         "type": "string",
         "description": "Search query to find relevant memories (searches both keys and content)"
       }
     },
     "required": ["query"]
   }
   ```

   **API Configuration:**
   - Method: `GET`
   - URL: `https://your-app-name.streamlit.app/?api=search_memory&query={{query}}`

### Usage Examples

**Store Information:**
```
User: "Remember, my name is John and I prefer dark mode"

Claude: [Calls store_memory]
  key: "user_name"
  content: "John"
  
  [Calls store_memory]
  key: "ui_preference"
  content: "dark mode"
```

**Retrieve Information:**
```
User: "What's my name?"

Claude: [Calls search_memory]
  query: "name"
  
Response: "Your name is John"
```

## Database Schema

```sql
CREATE TABLE memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
```

## Tech Stack

- **Backend:** Streamlit (Query Parameters API)
- **Database:** SQLite
- **Frontend:** Streamlit UI Components
- **Language:** Python 3.8+

## Why Pure Streamlit?

| Feature | Memoir-Core | Traditional FastAPI |
|---------|-------------|---------------------|
| Framework | Single (Streamlit) | Multiple (FastAPI + Frontend) |
| Deployment | One-click Streamlit Cloud | Requires server configuration |
| Testing | Browser URL | API client required |
| Port Management | Handled by Streamlit | Manual port exposure |
| Dependencies | 2 packages | 5+ packages |

## Project Structure

```
memoir-core/
├── app.py                 # Main Streamlit application
├── test_api.py           # API test suite
├── requirements.txt      # Python dependencies
├── claude_tools.json     # Claude tool configurations
└── README.md            # Documentation
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/memoir-core/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/memoir-core/discussions)
- **Documentation:** [Wiki](https://github.com/yourusername/memoir-core/wiki)

## Acknowledgments

- Built for the [Claude](https://claude.ai) AI assistant by Anthropic
- Powered by [Streamlit](https://streamlit.io)
- Database: [SQLite](https://www.sqlite.org)

---

<div align="center">

**Made by Evan William**

[⬆ Back to Top](#memoir-core)

</div>
