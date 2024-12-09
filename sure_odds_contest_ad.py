import requests
import tweepy
import random
import os
import schedule
import time

# Your Twitter API credentials
api_key = "F2MU6zhUDEPPcU3pOxfJq7J2Y"
api_secret = "jEBgijrY1Aigsy3bpVJldv4WFwshcr2RWFWqLhAeK5QMrKX7zJ"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAFgGrQEAAAAAcRPWLTcm5Dsd5Q%2F2cYcBSpdHnVo%3DzBRuxFGDKRBqLBr7gPzSp5qeGs5WK3dmC4va8n84FUSZSWyspR"
access_token = "1646168850147295234-Zw5P0wkecRHbXyTqXbT7JJbm264t8F"
access_token_secret = "gRK0iRZ0akKe7JQOL41xIYRJri9PtbmsTCqkmfEuDXt1V"

contest = [
    {
        "contestName": "Doink Sports",
        "imagePath": "./temp_image.jpg",
        "price": "Win a free 2 months subscription to Doink Sports",
        "twitterHandle": "@doink_sports",
    },
    {
        "contestName": "DG Fantasy",
        "imagePath": "./oGXbjunp_400x400.png",
        "price": "Win a free 2 months subscription to DG Fantasy",
        "twitterHandle": "@DGFantasy",
    },
    {
        "contestName": "PrizePicks",
        "imagePath": "./Po6QETC5_400x400.jpg",
        "price": "Win $100 to play on Prize Picks or whatever you want",
        "twitterHandle": "@PrizePicks",
    },
    {
        "contestName": "Underdog Fantasy",
        "imagePath": "./Qt3GgqWe_400x400.jpg",
        "price": "Win $100 to play on Underdog or whatever you want",
        "twitterHandle": "@UnderdogFantasy",
    }
]

# Authenticate with Twitter API
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

def send_tweet():
    selected_contest = random.choice(contest)
    message = (
        f"🚀 {selected_contest['contestName']} Contest! ({selected_contest['twitterHandle']})🏆\n"
        f"🏅 {selected_contest['price']}\n"
        f"🎉 Predict sports outcomes & win BIG!\n"
        f"💡 Free to play – Join now via the link in bio!\n"
        f"#GamblingX"
    )

    # Use the local image path from the contest data
    image_path = selected_contest['imagePath']

    # Upload the image to Twitter
    media = api.media_upload(image_path)

    # Post the tweet with the image using the v2 API
    client.create_tweet(text=message, media_ids=[media.media_id])

    print(f"Tweet sent: {message}")

# Schedule the tweet to be sent every 3 hours
schedule.every(3).hours.do(send_tweet)

while True:
    schedule.run_pending()
    time.sleep(1)