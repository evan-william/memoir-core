# Memoir-Core: Personal Memory Plugin for Claude

A persistent memory database that enables Claude to store and recall important information across conversations using Streamlit's query parameters API.

## Overview

Memoir-Core provides Claude with long-term memory capabilities through a lightweight SQLite database and a pure Streamlit interface. This allows Claude to remember user preferences, important facts, and context across different chat sessions without requiring complex infrastructure.

## Features

- **Persistent Memory Storage**: Information persists across sessions in a SQLite database
- **Smart Search**: Full-text search across memory keys and content
- **Web-Based UI**: Streamlit interface for manual memory management
- **API Integration**: Query parameter-based API for Claude integration
- **Zero Configuration**: Works out-of-the-box on Streamlit Cloud
- **Lightweight**: Minimal dependencies (Streamlit + Pandas)

## Architecture

```
┌─────────────────┐
│  Claude.ai      │
│  (Custom Tools) │
└────────┬────────┘
         │
         │ HTTPS GET Requests
         │ (Query Parameters)
         ▼
┌─────────────────┐
│ Streamlit App   │
│ (memoir-core)   │
├─────────────────┤
│ • Query Handler │
│ • Web UI        │
│ • API Endpoints │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ SQLite Database │
│ (memories.db)   │
└─────────────────┘
```

## Quick Start

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd memoir-core

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### Deployment to Streamlit Cloud

1. **Prepare Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Authenticate with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Note Your Deployment URL**
   - After deployment completes, you'll receive a URL like:
   - `https://your-app-name.streamlit.app`

## Claude Integration

### API Endpoints

The application exposes the following endpoints via query parameters:

| Endpoint | Parameters | Description |
|----------|------------|-------------|
| `/?api=health` | None | Health check endpoint |
| `/?api=store_memory` | `key`, `content` | Store a new memory |
| `/?api=search_memory` | `query` | Search memories |
| `/?api=get_memory` | `key` | Retrieve specific memory |

### Testing the API

Before configuring Claude, verify the API endpoints:

```bash
# Health check
https://your-app-name.streamlit.app/?api=health

# Store memory
https://your-app-name.streamlit.app/?api=store_memory&key=test&content=Hello%20World

# Search memory
https://your-app-name.streamlit.app/?api=search_memory&query=test

# Get memory
https://your-app-name.streamlit.app/?api=get_memory&key=test
```

### Claude Configuration

#### Step 1: Enable Custom Tools

1. Navigate to [claude.ai](https://claude.ai)
2. Open Settings (⚙️)
3. Select "Feature Preview" tab
4. Enable "Custom Tools"

#### Step 2: Configure store_memory Tool

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
- Headers: (leave empty)

#### Step 3: Configure search_memory Tool

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
- Headers: (leave empty)

## Usage Examples

### Storing Information

```
User: "My name is John and I prefer dark mode interfaces"
Claude: [Uses store_memory tool]
  - key: "user_name"
  - content: "John"
  
  [Uses store_memory tool]
  - key: "ui_preference"
  - content: "dark mode"
```

### Recalling Information

```
User: "What's my name again?"
Claude: [Uses search_memory tool]
  - query: "name"
  
Result: "Your name is John"
```

## Technical Details

### Dependencies

```
streamlit>=1.28.0
pandas>=2.0.0
```

### Database Schema

```sql
CREATE TABLE memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Why Pure Streamlit?

This implementation uses Streamlit's native query parameters instead of FastAPI for several advantages:

- **Simplicity**: No additional server framework required
- **Deployment**: Works immediately on Streamlit Cloud without configuration
- **Maintenance**: Single framework to manage
- **Testing**: Easy to test via browser URLs
- **Reliability**: Leverages Streamlit's built-in request handling

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the GitHub repository.

---

**Built for Claude users seeking persistent memory capabilities !**
