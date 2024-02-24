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

# Authenticate with Twitter API
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)



def post_message_with_image_on_twitter(tweet_id):


    message = (
        "Struggling with player prop research? Dive deep into insights and trends on Discord with Sure Odds – now FREE!\n\n"
        "💡📊 #PlayerProps #Research #SureOdds\n\n"
        "Check it out now: sure-odds.com"
    )

    # Path to the image file
    image_path = "path_to_your_image_file.jpg"  # Replace "path_to_your_image_file.jpg" with the actual path to your image file

    # Upload the image to Twitter
    media = api.media_upload(image_path)

    # Reply to the command post with the message and attached image
    client.create_tweet(text=message, media_ids=[media.media_id], in_reply_to_status_id=tweet_id)
    print("Message with image posted as reply on Twitter.")

def listen_for_mentions():
    # Listen for mentions of the bot's username
     for tweet in client.mentions_timeline():
        if tweet.user.screen_name == "sure_odds2023" and "run" in tweet.text.lower():
            # If the bot is mentioned with the "run" command, execute the function
            post_message_with_image_on_twitter(tweet.id)
            print("Executed function in response to mention.")
            break  # Break the loop after processing one command post

print("Script for posting optimized message with image and website link as reply on Twitter running")

# Schedule the script to check for mentions every minute
schedule.every(1).minutes.do(listen_for_mentions)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)