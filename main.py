from typing import Optional
from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import uvicorn

app = FastAPI()


def get_db_connection():
    """Establish a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="dell",
            password="1@Dell",
            database="post_tag_db"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        return None

@app.get("/")
def read_root():
    return {"message": "Welcome to Enhanced Blog Post Management with Tagging"}

@app.post("/create_post")
def create_post(
    title: str = Body(...), 
    content: str = Body(...), 
    tags: Optional[str] = Body(None)
):
    """Create a new blog post."""
    conn = get_db_connection()
    if conn is None:
        return {"error": "Database connection failed"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        post_id = cursor.lastrowid
        print(f"✅ Post created with ID: {post_id}")
        if tags:
            tags = [tag.strip().lower() for tag in tags.split(",")]
            for tag in tags:
                if not tag:
                    continue
                cursor.execute("INSERT IGNORE INTO tags (name) VALUES (%s)", (tag,))
                cursor.execute("SELECT id FROM tags WHERE name = %s", (tag,))
                tag_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (%s, %s)", (post_id, tag_id))
        conn.commit()
        return {"message": "Post created successfully"}
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()

@app.get("/get_posts")
def get_posts():
    """Retrieve all blog posts with their tags."""
    conn = get_db_connection()
    if conn is None:
        return {"error": "Database connection failed"}
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id, p.title, GROUP_CONCAT(t.name) AS tags
            FROM posts p
            LEFT JOIN post_tags pt ON p.id = pt.post_id
            LEFT JOIN tags t ON pt.tag_id = t.id
            GROUP BY p.id
        """)
        posts = cursor.fetchall()
        print(f"✅ Retrieved {len(posts)} posts")
        return posts
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}
    finally:
        conn.close()

@app.get("/get_post/{post_title}")
def get_post(post_title: str):
    """Retrieve a specific blog post by title."""
    conn = get_db_connection()
    if conn is None:
        return {"error": "Database connection failed"}
    
    try:
        post_title = post_title.strip().lower()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id, p.title, p.content, GROUP_CONCAT(t.name) AS tags
            FROM posts p
            LEFT JOIN post_tags pt ON p.id = pt.post_id
            LEFT JOIN tags t ON pt.tag_id = t.id
            WHERE p.title = %s
            GROUP BY p.id
        """, (post_title,))
        posts = cursor.fetchall()
        if posts:
            print(f"✅ Retrieved post: {len(posts)}")
            return posts
        else:
            raise HTTPException(status_code=404, detail="Post not found")
            print("❌ No post found")
            return {"error": "No post found"}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}
    finally:
        conn.close()

@app.get("/get_posts_by_tag/{tag_name}")
def get_posts_by_tag(tag_name: str):
    """Retrieve all blog posts associated with a specific tag."""
    conn = get_db_connection()
    if conn is None:
        return {"error": "Database connection failed"}
    
    try:
        tag_name = tag_name.strip().lower()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id, p.title, GROUP_CONCAT(t.name) AS tags
            FROM posts p
            LEFT JOIN post_tags pt ON p.id = pt.post_id
            LEFT JOIN tags t ON pt.tag_id = t.id
            WHERE t.name = %s
            GROUP BY p.id
        """, (tag_name,))
        posts = cursor.fetchall()
        if posts:
            print(f"✅ Retrieved {len(posts)} posts for tag: {tag_name}")
            return posts
        else:
            raise HTTPException(status_code=404, detail="No posts found for this tag")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}
    finally:
        conn.close()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)