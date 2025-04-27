# FastAPI Blog Post Management with Tagging

This project is a blog post management system built with FastAPI, MySQL, and Click. It allows users to create, retrieve, and search for blog posts and associated tags. The system supports the following actions:

- **Creating new blog posts** with optional tags.
- **Retrieving all posts** and filtering by tags.
- **Retrieving specific posts** by title.

Additionally, this project includes a Command-Line Interface (CLI) for interacting with the blog post system.

## Requirements

- Python 3.7 or higher
- MySQL Server
- FastAPI
- Uvicorn
- `requests` (for CLI requests)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/blog-post-management.git
cd blog-post-management
```

### 2. Create a Python Virtual Environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate  # For Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up MySQL Database

Make sure you have MySQL installed and running. Then, run the `db.py` script to create the necessary database, tables, and sample data.

```bash
python db.py
```

This will create a database called `post_tag_db` with tables for `posts`, `tags`, and `post_tags`. It will also insert sample data.

### 5. Run the FastAPI server

Start the FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## CLI Usage

This project includes a CLI (`cli.py`) to interact with the blog posts via HTTP requests.

### 1. Create a New Post

To create a new post, use the `create_post` command:

```bash
python cli.py create-post "Post Title" "Post Content" --tags "tag1,tag2"
```

Example:

```bash
python cli.py create-post "New Blog Post" "This is my first blog post!" --tags "Tech, Python"
```

This will create a new post with the specified title, content, and tags.

### 2. Get All Posts

To retrieve all posts:

```bash
python cli.py get-posts
```

This will display all posts with their associated tags.

### 3. Get a Post by Title

To retrieve a post by title:

```bash
python cli.py get-posts-by-title "Post Title"
```

Example:

```bash
python cli.py get-posts-by-title "New Blog Post"
```

This will return the post with the matching title, along with its content and tags.

### 4. Get Posts by Tag

To retrieve posts by a specific tag:

```bash
python cli.py get-posts-by-tag "TagName"
```

Example:

```bash
python cli.py get-posts-by-tag "Tech"
```

This will return all posts associated with the tag "Tech".

## API Endpoints

### 1. `POST /create_post`

Creates a new blog post. Accepts a JSON body with `title`, `content`, and optional `tags` (comma-separated list).

Example Request:

```json
{
  "title": "New Blog Post",
  "content": "This is my first blog post!",
  "tags": "Tech, Python"
}
```

### 2. `GET /get_posts`

Retrieves all blog posts with their associated tags.

### 3. `GET /get_post/{post_title}`

Retrieves a specific blog post by its title.

### 4. `GET /get_posts_by_tag/{tag_name}`

Retrieves all blog posts associated with a specific tag.

## Project Structure

```
blog-post-management/
├── cli.py               # Command-line interface for interacting with the API
├── db.py                # Script for setting up MySQL database and inserting sample data
├── main.py              # FastAPI application with endpoints
├── requirements.txt     # List of dependencies
└── README.md            # Project documentation (you're reading it!)
```

## Troubleshooting

- **Database Connection Issues:** Ensure that MySQL is installed, running, and accessible with the correct credentials (host, user, password).
- **Missing Packages:** If you encounter errors related to missing Python packages, run `pip install -r requirements.txt` to install the necessary dependencies.

## License

This project is licensed under the MIT License.