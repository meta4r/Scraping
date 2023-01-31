import praw
import requests
import os

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='')

subreddit = reddit.subreddit('occult')
posts = subreddit.hot(limit=10)

data = []

print("Scraping data from subreddit...")

for post in posts:
    post_data = {}
    post_data['title'] = post.title
    post_data['text'] = post.selftext

    comments = []
    for comment in post.comments.list():
        if isinstance(comment, praw.models.Comment):
            comment_str = str(comment.body.encode('utf-8'), 'utf-8')
            comments.append(comment_str)
    post_data['comments'] = comments

    if post.url.endswith(".jpg") or post.url.endswith(".png") or post.url.endswith(".gif"):
        response = requests.get(post.url)
        if response.status_code == 200:
            with open(os.path.join("images", post.id + os.path.splitext(post.url)[1]), "wb") as f:
                f.write(response.content)
        post_data['image_url'] = post.id + os.path.splitext(post.url)[1]

    data.append(post_data)

html = "<html><head><title>Subreddit Scraped Data</title></head><body>"

for post in data:
    html += "<h2>" + post['title'] + "</h2>"
    html += "<p>" + post['text'] + "</p>"
    
    if 'image_url' in post:
        html += "<img src='images/" + post['image_url'] + "'>"
    
    html += "<ul>"
    for comment in post['comments']:
        html += "<li>" + comment + "</li>"
    html += "</ul>"

html += "</body></html>"

with open('data.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Data collected and written to data.html")