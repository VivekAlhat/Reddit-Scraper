import os
import praw
import config
import requests
from PIL import Image
from io import BytesIO

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=config.user_agent,
                     username=config.username,
                     password=config.password)

Term = input("Enter Subreddit: ")
subreddit = reddit.subreddit(Term)

for post in subreddit.hot():
    url = str(post.url)
    timestamp = post.created_utc
    if url.endswith("jpg") or url.endswith("gif") or url.endswith("png") or url.endswith("jpeg"):
        req = requests.get(url)
        img = Image.open(BytesIO(req.content))
        if(os.path.isdir("./Reddit/{}".format(subreddit))):
            img.save("./Reddit/{}/{}.{}".format(subreddit,
                                                timestamp, (img.format).lower()))
        else:
            print("First time? creating directory for this subreddit")
            os.mkdir("./Reddit/{}".format(subreddit))
            img.save("./Reddit/{}/{}.{}".format(subreddit,
                                                timestamp, (img.format).lower()))
        print("{}.{} saved to disk.".format(timestamp, (img.format).lower()))
