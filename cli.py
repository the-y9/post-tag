import click
import requests
from typing import Optional

BASE_URL = "http://127.0.0.1:8000"

def send_request(endpoint: str, method: str = "GET", params: Optional[dict] = None, data: Optional[dict] = None):
    url = f"{BASE_URL}/{endpoint}"
    response = None
    if method == "GET":
        response = requests.get(url, params=params)
    elif method == "POST":
        response = requests.post(url, json=data)

    if response:
        return response.json()
    return None


@click.group()
def cli():
    """CLI for interacting with the FastAPI Blog Post Management."""
    pass


@click.command()
@click.argument('title')
@click.argument('content')
@click.option('--tags', default=None, help='Comma-separated tags for the post.')
def create_post(title: str, content: str, tags: Optional[str]):
    """Create a new blog post."""
    data = {
        "title": title,
        "content": content,
        "tags": tags
    }
    response = send_request("create_post", method="POST", data=data)
    if response:
        print(f"Post created successfully: {response.get('message')}")
    else:
        print("Error creating post.")


@click.command()
def get_posts():
    """Retrieve all blog posts with their tags."""
    response = send_request("get_posts")
    if response:
        for post in response:
            print(f"ID: {post['id']}, Title: {post['title']}, Tags: {post['tags']}")
    else:
        print("Error retrieving posts.")


@click.command()
@click.argument('post_title')
def get_posts_by_title(post_title: str):
    """Retrieve a specific blog post by title."""
    response = send_request(f"get_post/{post_title}")
    if response:
        post = response[0]  # Assuming a single post is returned
        print(f"Title: {post['title']}\nContent: {post['content']}\nTags: {post['tags']}")
    else:
        print("Error retrieving post.")


@click.command()
@click.argument('tag_name')
def get_posts_by_tag(tag_name: str):
    """Retrieve all blog posts associated with a specific tag."""
    response = send_request(f"get_posts_by_tag/{tag_name}")
    if response:
        for post in response:
            print(f"ID: {post['id']}, Title: {post['title']}, Tags: {post['tags']}")
    else:
        print("Error retrieving posts by tag.")


# Add the commands to the CLI
cli.add_command(create_post)
cli.add_command(get_posts)
cli.add_command(get_posts_by_title)
cli.add_command(get_posts_by_tag)

if __name__ == "__main__":
    cli()
