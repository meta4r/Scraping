import requests
import os
import praw
import datetime

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='')

subreddit_name = 'list-palestine'
subreddit = reddit.subreddit(subreddit_name)
posts = subreddit.new(limit=10)

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
            images_folder = os.path.join(subreddit_name, "images")
            os.makedirs(images_folder, exist_ok=True)
            with open(os.path.join(images_folder, post.id + os.path.splitext(post.url)[1]), "wb") as f:
                f.write(response.content)
        post_data['image_url'] = post.id + os.path.splitext(post.url)[1]

    data.append(post_data)

html = "<html><head><title>" + subreddit_name + " Scraped Data</title></head><body>"

for post in data:
    html += "<h2>" + post['title'] + "</h2>"
    html += "<p>" + post['text'] + "</p>"
    
    if 'image_url' in post:
        html += "<img src='" + os.path.join("images", post['image_url']) + "'>"
    
    html += "<ul>"
    for comment in post['comments']:
        html += "<li>" + comment + "</li>"
    html += "</ul>"

html += "</body></html>"

os.makedirs(subreddit_name, exist_ok=True)
current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = subreddit_name + "_" + current_time + ".html"
file_path = os.path.join(subreddit_name, file_name)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)