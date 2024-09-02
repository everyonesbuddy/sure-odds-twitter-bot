import requests
import tweepy
from datetime import datetime, timedelta
import pytz
import schedule
import time

# Your Twitter API credentials
api_key = "F2MU6zhUDEPPcU3pOxfJq7J2Y"
api_secret = "jEBgijrY1Aigsy3bpVJldv4WFwshcr2RWFWqLhAeK5QMrKX7zJ"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAFgGrQEAAAAAcRPWLTcm5Dsd5Q%2F2cYcBSpdHnVo%3DzBRuxFGDKRBqLBr7gPzSp5qeGs5WK3dmC4va8n84FUSZSWyspR"
access_token = "1646168850147295234-Zw5P0wkecRHbXyTqXbT7JJbm264t8F"
access_token_secret = "gRK0iRZ0akKe7JQOL41xIYRJri9PtbmsTCqkmfEuDXt1V"


def call_sure_odds_ads():
    # Authenticate with Twitter API
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    message = (
        "🎉 Africa's #1 Free-to-Play Sports Predictions Contest! 🎉\n"
        "🏆 Showcase Your Sports Knowledge and stand a chance to win 1,000,000 Naira (or $500 USD) monthly—risk-free! 🤑\n"
        "🚀 Join Now and Don’t Miss Out!\n"
        "https://sure-odds.com/ #Sports #Contests #WinBig #FreeToPlay #sureodds"
    )

    # Path to the image file
    image_path1 = "./Yellow And Green Raffle Contest Poster.png"

    # Upload the images to Twitter
    media1 = api.media_upload(image_path1)

        # Post the message on Twitter
    client.create_tweet(text=message, media_ids=[media1.media_id])
    # client.create_tweet(text=message)
    print("Message posted on Twitter.")

    print("Script for posting optimized message on Twitter running")

# call_sure_odds_automated_marketing()

# Set the Eastern Time (EST) timezone
est = pytz.timezone('US/Eastern')

## Schedule the script to run at specific times
schedule.every().day.at("12:00").do(call_sure_odds_ads).timezone = est

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)