import mysql.connector

host = "localhost"
port = 3306
user = "dell"
password = "1@Dell"

try:
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
    )
    cursor = conn.cursor()
    print(f"✅ Connected to MySQL as {user}.")
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
    exit()

# Step 1: Create database (if it doesn't exist)
try:
    database_name = "post_tag_db"
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    cursor.execute(f"USE {database_name}")
    print(f"✅ Using database: {database_name}")
except mysql.connector.Error as err:
    print(f"❌ Failed connecting database '{database_name}': {err}")
    exit()

# Step 4: Create a table
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            content TEXT
        )
    """)
    print("✅ Table 'posts' created or already exists.")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        )
    """)
    print("✅ Table 'tags' created or already exists.")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS post_tags (
            post_id INT,
            tag_id INT,
            PRIMARY KEY (post_id, tag_id),
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
        )
    """)
    print("✅ Table 'post_tags' created or already exists.")
except mysql.connector.Error as err:
    print(f"❌ Failed creating table: {err}")
    exit()

# Step 5: Insert sample data
try:
    post_query = "INSERT INTO posts (title, content) VALUES (%s, %s)"
    post_data = [
        ("New Beginnings", "Try Harder!"),
        ("The dark Knigh", "Will Rise!"),
        ("Tutenkhamen", "The General of After World!"),
    ]

    tag_query = "INSERT INTO tags (name) VALUES (%s)"
    tag_data = [
        ("Movie",),
        ("Book",),
    ]

    post_tag_query = "INSERT INTO post_tags (post_id, tag_id) VALUES (%s, %s)"
    post_tag_data = [
        (4, 4),  # First Post with Python
        (4, 5),  # First Post with MySQL
        (5, 4),  # Second Post with Database
        (6, 5),  # Third Post with Python
    ]
    cursor.executemany(post_query, post_data)
    print("✅ Post data inserted into 'posts'.")

    cursor.executemany(tag_query, tag_data)
    print("✅ Tag data inserted into 'tags'.")

    cursor.executemany(post_tag_query, post_tag_data)
    print("✅ Post-Tag data inserted into 'post_tags'.")

    conn.commit()
except mysql.connector.Error as err:
    print(f"❌ Failed inserting data: {err}")

# Step 6: Read and print data
try:
    cursor.execute('''
SELECT
    posts.id,
    posts.title,
    posts.content,
    GROUP_CONCAT(CONCAT('[', tags.name, ']') SEPARATOR ', ') AS tags
FROM posts
JOIN post_tags ON posts.id = post_tags.post_id
JOIN tags ON tags.id = post_tags.tag_id
GROUP BY posts.id, posts.title, posts.content
ORDER BY posts.id;
    ''')
    for (post_id, title, content, tag_name) in cursor.fetchall():
        print(f"{post_id}. {title} — {content} [{tag_name}]")

    cursor.close()
    conn.close()
except Exception as err:
    print(f"❌ Failed reading data: {err}")