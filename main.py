import os
import art
import praw
import config
import easygui
import requests
from PIL import Image
from io import BytesIO

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=config.user_agent,
                     username=config.username,
                     password=config.password)

print(art.text2art("Reddit Scraper", font="cybermedium"))

print("1. Scrape Subreddit \n2. Scrape User\n")
choice = int(input("Choose your option: "))

if choice == 1:
    term = input("Subreddit: /r/")
    subreddit = reddit.subreddit(term)

    p = easygui.diropenbox(
        msg="Select directory to store files", title="Choose directory")

    print("Currently scraping {}'s posts".format(subreddit))
    for post in subreddit.new():
        url = str(post.url)
        timestamp = post.created_utc
        if url.endswith("jpg") or url.endswith("gif") or url.endswith("png") or url.endswith("jpeg"):
            req = requests.get(url)
            img = Image.open(BytesIO(req.content))

            if(not (os.path.isdir(p+"/Scraper/{}".format(subreddit)))):
                print("First time? creating directory for this subreddit")
                os.makedirs(p+"/Scraper/{}".format(subreddit))

            img.save(p+"/Scraper/{}/{}.{}".format(subreddit,
                                                  timestamp, (img.format).lower()))
            print("{}.{} saved to disk.".format(
                timestamp, (img.format).lower()))
elif choice == 2:
    user = input("User: /u/")
    userInfo = open(user+".txt", "w")

    # Get user's 10 new submissions
    userInfo.write("--- New Submissions ---\n")
    for submission in reddit.redditor(user).submissions.new(limit=10):
        userInfo.write(submission.url + "\n")

    userInfo.write('\n')

    # Get user's 10 top submissions
    userInfo.write("--- Top Submissions ---\n")
    for submission in reddit.redditor(user).submissions.top(limit=10):
        userInfo.write(submission.url + "\n")

    userInfo.write('\n')

    # Get user's trophy list
    userInfo.write("--- Trophy Collection ---\n")
    for trophy in reddit.redditor("spez").trophies():
        userInfo.write(trophy.name)

    print(user+".txt saved to disk")
else:
    print("Please, select valid option")
