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
        "🚀 Tired of losing bets and following unreliable handicappers? Discover Sure Odds and find top experts based on verified performance! Start betting smarter today. 💡🔝 https://sure-odds.com/ #SportsBetting #BettingTips #GamblingTwitter"
    )

    # Path to the image file
    image_path = "./Screenshot 2024-07-28 124520.png"

    # Upload the image to Twitter
    media = api.media_upload(image_path)

        # Post the message on Twitter
    client.create_tweet(text=message , media_ids=[media.media_id])
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