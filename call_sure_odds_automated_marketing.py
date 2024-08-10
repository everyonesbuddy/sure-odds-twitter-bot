import requests
import tweepy
from datetime import datetime
import pytz
import schedule
import time

# Your Twitter API credentials
api_key = "F2MU6zhUDEPPcU3pOxfJq7J2Y"
api_secret = "jEBgijrY1Aigsy3bpVJldv4WFwshcr2RWFWqLhAeK5QMrKX7zJ"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAFgGrQEAAAAAcRPWLTcm5Dsd5Q%2F2cYcBSpdHnVo%3DzBRuxFGDKRBqLBr7gPzSp5qeGs5WK3dmC4va8n84FUSZSWyspR"
access_token = "1646168850147295234-Zw5P0wkecRHbXyTqXbT7JJbm264t8F"
access_token_secret = "gRK0iRZ0akKe7JQOL41xIYRJri9PtbmsTCqkmfEuDXt1V"



def call_sure_odds_automated_marketing():
    # Authenticate with Twitter API
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    message = (
        "🚀 Boost Your Server with Top Sports Cappers from Sure Odds! 🏆\n"
        "Enhance your sports Discord with expert insights. Add 10+ top cappers today! 📈\n"
        "Exclusive Picks: Daily picks from top cappers. 📊\n"
        "Leaderboard: Real-time rankings. 🥇\n"
        "https://sure-odds.com/ #SportsBetting #BettingTips #GamblingTwitter"
    )

    # Path to the image file
    image_path1 = "./Screenshot 2024-08-10 015626.png"
    image_path2 = "./Screenshot 2024-08-10 015737.png"

    # Upload the images to Twitter
    media1 = api.media_upload(image_path1)
    media2 = api.media_upload(image_path2)

        # Post the message on Twitter
    client.create_tweet(text=message, media_ids=[media1.media_id, media2.media_id])
    print("Message posted on Twitter.")
    print(message)

    print("Script for posting optimized message on Twitter running")



# Set the Eastern Time (EST) timezone
est = pytz.timezone('US/Eastern')

## Schedule the script to run at specific times
schedule.every().day.at("11:00").do(call_sure_odds_automated_marketing).timezone = est

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)