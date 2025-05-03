import os
import frontmatter
import requests

POSTS_DIR = "src/content/blog"
API_KEY = os.getenv("DEVTO_API_KEY")
HEADERS = {"api-key": API_KEY, "Content-Type": "application/json"}

def find_md_files():
    for root, _, files in os.walk(POSTS_DIR):
        for f in files:
            if f.endswith(".md"):
                yield os.path.join(root, f)

def publish_post(filepath):
    with open(filepath, encoding="utf-8") as f:
        post = frontmatter.load(f)
    
    if not post.get("devto", False):
        return

    data = {
        "title": post.get("title", "Untitled"),
        "published": post.get("published", False),
        "tags": post.get("tags", []),
        "body_markdown": post.content
    }

    response = requests.post("https://dev.to/api/articles", headers=HEADERS, json={"article": data})
    if response.status_code == 201:
        print(f"✅ Published: {data['title']}")
    else:
        print(f"❌ Failed to publish {data['title']} — {response.status_code}: {response.text}")

if __name__ == "__main__":
    for path in find_md_files():
        publish_post(path)
