from flask import Flask
from flask import render_template
import tweepy

app = Flask(__name__)


@app.route('/')
def image_caption():
    return render_template('ImageMLWebsite.html')

def tweet(image, caption):
    auth = tweepy.OAuthHandler(
        "s6j20sJFJRabXx5ImyM0QEEaD", "N6MmSc19jfCqESX3wAInJUhLEW0oidUptDiMNF6XgPahgqnSYg")
    auth.set_access_token("2733437449-7tAXSHbYjQJapC9ITqxLmsDtHCcHcwDhL6AJ0Lf",
                          "ih6BSfqlTAV4eYE5MzrzBeqhYXZMkbWSYQ7FclXATKUen")
    
    tweet_text = caption
    image_path = image
    status = api.update_with_media(image_path, caption)
    api = tweepy.API(auth)
    api.update_status(status=tweet_text)
