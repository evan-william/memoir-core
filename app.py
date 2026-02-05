"""
Memoir-Core: Personal Memory Plugin untuk Claude (Pure Streamlit Version)
Database memori jangka panjang dengan Streamlit UI dan API via Query Parameters
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import json
from typing import Optional

# ==================== DATABASE SETUP ====================

DB_NAME = "memoir_core.db"

def init_database():
    """Inisialisasi database SQLite"""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_connection():
    """Membuat koneksi database thread-safe"""
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# ==================== API FUNCTIONS ====================

def store_memory_api(key: str, content: str) -> dict:
    """API function untuk menyimpan memori"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        
        # Cek apakah key sudah ada
        cursor.execute("SELECT id FROM memories WHERE key = ?", (key,))
        existing = cursor.fetchone()
        
        if existing:
            # Update jika sudah ada
            cursor.execute(
                "UPDATE memories SET content = ?, timestamp = ? WHERE key = ?",
                (content, timestamp, key)
            )
            message = f"Memory updated for key: {key}"
        else:
            # Insert jika belum ada
            cursor.execute(
                "INSERT INTO memories (key, content, timestamp) VALUES (?, ?, ?)",
                (key, content, timestamp)
            )
            message = f"Memory stored with key: {key}"
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": message,
            "data": {"key": key, "timestamp": timestamp}
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "data": None
        }

def search_memory_api(query: str) -> dict:
    """API function untuk mencari memori"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Pencarian case-insensitive pada key dan content
        query_pattern = f"%{query}%"
        cursor.execute(
            """
            SELECT key, content, timestamp FROM memories 
            WHERE key LIKE ? OR content LIKE ?
            ORDER BY timestamp DESC
            """,
            (query_pattern, query_pattern)
        )
        
        results = cursor.fetchall()
        conn.close()
        
        memories = [
            {
                "key": row[0],
                "content": row[1],
                "timestamp": row[2]
            }
            for row in results
        ]
        
        return {
            "success": True,
            "message": f"Found {len(memories)} memory/memories",
            "data": {"memories": memories, "count": len(memories)}
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "data": None
        }

def get_memory_api(key: str) -> dict:
    """API function untuk mengambil memori spesifik"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT key, content, timestamp FROM memories WHERE key = ?",
            (key,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "success": True,
                "message": f"Memory found for key: {key}",
                "data": {
                    "key": result[0],
                    "content": result[1],
                    "timestamp": result[2]
                }
            }
        else:
            return {
                "success": False,
                "message": f"No memory found for key: {key}",
                "data": None
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "data": None
        }

# ==================== API HANDLER ====================

def handle_api_request():
    """Handle API requests via query parameters"""
    params = st.query_params
    
    # Check if this is an API request
    if "api" in params:
        action = params.get("api")
        
        if action == "store_memory":
            key = params.get("key", "")
            content = params.get("content", "")
            
            if not key or not content:
                result = {
                    "success": False,
                    "message": "Missing required parameters: key and content"
                }
            else:
                result = store_memory_api(key, content)
            
            # Display JSON response
            st.json(result)
            st.stop()
        
        elif action == "search_memory":
            query = params.get("query", "")
            
            if not query:
                result = {
                    "success": False,
                    "message": "Missing required parameter: query"
                }
            else:
                result = search_memory_api(query)
            
            st.json(result)
            st.stop()
        
        elif action == "get_memory":
            key = params.get("key", "")
            
            if not key:
                result = {
                    "success": False,
                    "message": "Missing required parameter: key"
                }
            else:
                result = get_memory_api(key)
            
            st.json(result)
            st.stop()
        
        elif action == "health":
            result = {
                "status": "healthy",
                "service": "Memoir-Core API"
            }
            st.json(result)
            st.stop()

# ==================== STREAMLIT UI ====================

def main():
    """Aplikasi Streamlit utama"""
    
    # Inisialisasi database
    init_database()
    
    # Handle API requests first
    handle_api_request()
    
    # Page config
    st.set_page_config(
        page_title="Memoir-Core",
        page_icon="🧠",
        layout="wide"
    )
    
    # Header
    st.title("🧠 Memoir-Core")
    st.markdown("**Personal Memory Plugin untuk Claude** | Database memori jangka panjang")
    st.divider()
    
    # Sidebar - API Info
    with st.sidebar:
        st.header("📡 API Information")
        
        # Get base URL
        try:
            base_url = st.get_option("browser.serverAddress")
            if not base_url or base_url == "localhost":
                base_url = "http://localhost:8501"
            elif not base_url.startswith("http"):
                base_url = f"https://{base_url}"
        except:
            base_url = "http://localhost:8501"
        
        st.info(f"**Base URL:** `{base_url}`")
        
        st.markdown("### API Endpoints:")
        st.code(f"{base_url}/?api=store_memory&key={{key}}&content={{content}}", language="text")
        st.code(f"{base_url}/?api=search_memory&query={{query}}", language="text")
        st.code(f"{base_url}/?api=get_memory&key={{key}}", language="text")
        st.code(f"{base_url}/?api=health", language="text")
        
        st.markdown("### Quick Test:")
        if st.button("🔍 Health Check"):
            st.success("✅ API is running!")
        
        st.divider()
        st.markdown("### Statistics:")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM memories")
        count = cursor.fetchone()[0]
        conn.close()
        st.metric("Total Memories", count)
    
    # Main content - Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 View Memories", "➕ Add Memory", "🔍 Search", "⚙️ Setup Guide"])
    
    # TAB 1: View Memories
    with tab1:
        st.header("All Stored Memories")
        
        conn = get_connection()
        df = pd.read_sql_query(
            "SELECT id, key, content, timestamp FROM memories ORDER BY timestamp DESC",
            conn
        )
        conn.close()
        
        if not df.empty:
            # Display options
            col1, col2 = st.columns([3, 1])
            with col2:
                show_id = st.checkbox("Show ID", value=False)
            
            # Display dataframe
            if show_id:
                st.dataframe(df, use_container_width=True, height=400)
            else:
                st.dataframe(df.drop(columns=['id']), use_container_width=True, height=400)
            
            # Delete memory
            st.subheader("Delete Memory")
            col1, col2 = st.columns([3, 1])
            with col1:
                key_to_delete = st.selectbox(
                    "Select memory key to delete:",
                    options=df['key'].tolist()
                )
            with col2:
                st.write("")  # Spacer
                st.write("")  # Spacer
                if st.button("🗑️ Delete", type="secondary"):
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM memories WHERE key = ?", (key_to_delete,))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ Deleted memory: {key_to_delete}")
                    st.rerun()
        else:
            st.info("📭 No memories stored yet. Add your first memory in the 'Add Memory' tab!")
    
    # TAB 2: Add Memory
    with tab2:
        st.header("Add New Memory")
        
        with st.form("add_memory_form"):
            key_input = st.text_input(
                "Memory Key*",
                placeholder="e.g., user_preferences, favorite_book, project_deadline",
                help="Unique identifier for this memory"
            )
            
            content_input = st.text_area(
                "Memory Content*",
                placeholder="Enter the information you want to store...",
                help="The actual information to remember",
                height=150
            )
            
            submitted = st.form_submit_button("💾 Save Memory", type="primary")
            
            if submitted:
                if not key_input or not content_input:
                    st.error("❌ Both key and content are required!")
                else:
                    result = store_memory_api(key_input, content_input)
                    if result["success"]:
                        if "updated" in result["message"].lower():
                            st.warning(f"⚠️ {result['message']}")
                        else:
                            st.success(f"✅ {result['message']}")
                        st.rerun()
                    else:
                        st.error(f"❌ {result['message']}")
    
    # TAB 3: Search
    with tab3:
        st.header("Search Memories")
        
        search_query = st.text_input(
            "🔍 Search Query",
            placeholder="Enter keywords to search in keys and content...",
            help="Search is case-insensitive and looks in both keys and content"
        )
        
        if search_query:
            result = search_memory_api(search_query)
            
            if result["success"] and result["data"]["count"] > 0:
                st.success(f"Found {result['data']['count']} result(s)")
                df_search = pd.DataFrame(result["data"]["memories"])
                st.dataframe(df_search, use_container_width=True, height=400)
            else:
                st.warning("No memories found matching your query.")
        else:
            st.info("👆 Enter a search query above to find memories")
    
    # TAB 4: Setup Guide
    with tab4:
        st.header("⚙️ Setup Guide for Claude Integration")
        
        st.markdown("""
        ### Step 1: Deploy to Streamlit Cloud
        
        1. Push kode ini ke GitHub repository
        2. Buka [share.streamlit.io](https://share.streamlit.io)
        3. Deploy repository Anda
        4. Catat URL deployment (e.g., `https://your-app.streamlit.app`)
        
        ### Step 2: Configure Claude Custom Tools
        
        Buka pengaturan Claude dan tambahkan **Custom Tool** dengan JSON Schema berikut:
        """)
        
        # Encode example for URL
        import urllib.parse
        
        # JSON Schema untuk Claude
        schema_store = {
            "name": "store_memory",
            "description": "Store important information to long-term memory database. Use this to remember user preferences, facts, or any information that should persist across conversations.",
            "input_schema": {
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
        }
        
        schema_search = {
            "name": "search_memory",
            "description": "Search for information in the long-term memory database. Use this to recall previously stored information.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find relevant memories (searches both keys and content)"
                    }
                },
                "required": ["query"]
            }
        }
        
        st.subheader("📝 Tool 1: store_memory")
        st.json(schema_store)
        
        st.markdown("**API Configuration:**")
        st.code(f"""
Method: GET
URL: {base_url}/?api=store_memory&key={{{{key}}}}&content={{{{content}}}}
Headers: None required
        """, language="text")
        
        st.divider()
        
        st.subheader("🔍 Tool 2: search_memory")
        st.json(schema_search)
        
        st.markdown("**API Configuration:**")
        st.code(f"""
Method: GET
URL: {base_url}/?api=search_memory&query={{{{query}}}}
Headers: None required
        """, language="text")
        
        st.divider()
        
        st.markdown("""
        ### Step 3: Test the Integration
        
        Setelah setup selesai, coba chat dengan Claude:
        
        - **"Ingat ya, makanan favorit saya adalah nasi goreng"**
          → Claude akan memanggil `store_memory` dengan key seperti `favorite_food`
        
        - **"Apa makanan favorit saya?"**
          → Claude akan memanggil `search_memory` dengan query `favorite food`
        
        ### Example URLs:
        
        Test langsung di browser:
        """)
        
        # Example URLs
        example_key = "test_key"
        example_content = "This is a test memory"
        example_query = "test"
        
        st.code(f"{base_url}/?api=health", language="text")
        st.code(f"{base_url}/?api=store_memory&key={example_key}&content={urllib.parse.quote(example_content)}", language="text")
        st.code(f"{base_url}/?api=search_memory&query={example_query}", language="text")
        st.code(f"{base_url}/?api=get_memory&key={example_key}", language="text")
        
        st.markdown("""
        ### Notes:
        
        - 🔒 **Security**: Database SQLite tersimpan di Streamlit Cloud. Untuk production, pertimbangkan enkripsi atau database cloud
        - 🔄 **Persistence**: File database akan persist selama app tidak di-restart atau re-deploy
        - 📊 **Monitoring**: Gunakan tab "View Memories" untuk melihat semua data yang tersimpan
        - ⚠️ **URL Encoding**: Content dengan spasi/special characters akan otomatis di-encode oleh Claude
        - ✅ **Simple**: Menggunakan GET requests via query params, lebih simple untuk Streamlit Cloud
        """)
        
        st.success("✅ Setup complete! Your Memoir-Core is ready to use with Claude.")

if __name__ == "__main__":
    main()