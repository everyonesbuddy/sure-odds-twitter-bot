import requests
import tweepy
from datetime import datetime, timedelta
import pytz
import schedule
import time
import random

# Your Twitter API credentials
api_key = "F2MU6zhUDEPPcU3pOxfJq7J2Y"
api_secret = "jEBgijrY1Aigsy3bpVJldv4WFwshcr2RWFWqLhAeK5QMrKX7zJ"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAFgGrQEAAAAAcRPWLTcm5Dsd5Q%2F2cYcBSpdHnVo%3DzBRuxFGDKRBqLBr7gPzSp5qeGs5WK3dmC4va8n84FUSZSWyspR"
access_token = "1646168850147295234-Zw5P0wkecRHbXyTqXbT7JJbm264t8F"
access_token_secret = "gRK0iRZ0akKe7JQOL41xIYRJri9PtbmsTCqkmfEuDXt1V"


def call_sure_odds_automated_wins_loss_marketing():
    url = "https://sheet.best/api/sheets/b9c7054b-1a70-4afb-9a14-c49967e8faf8"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Get last two day's date in the required format
        lasttwodays = (datetime.utcnow() - timedelta(days=2)).strftime('%Y-%m-%d')

        # Filter the data
        filtered_data = [
            game for game in data
            if game['betResult'] is not None and game['gameCommenceTime'].startswith(lasttwodays)
        ]

        if not filtered_data:
            print("No games found for today with betResult as null.")
            return

        # Print the filtered data
        print(filtered_data)

        # Randomly select a game from the filtered data
        selected_game = random.choice(filtered_data)

        # Determine the username display format based on socialType
        if selected_game['socialType'] == 'twitter':
            username_display = f"@{selected_game['twitterUsername']}"
        else:
            username_display = selected_game['twitterUsername']

            # Replace underscores with spaces in league and market
        league = selected_game['league'].replace('_', ' ')
        market = selected_game['market'].replace('_', ' ')

       # Format the gameCommenceTime to a more readable format in EST
        game_time = datetime.strptime(selected_game['gameCommenceTime'], '%Y-%m-%dT%H:%M:%SZ')
        game_time_utc = game_time.replace(tzinfo=pytz.utc)
        game_time_est = game_time_utc.astimezone(pytz.timezone('US/Eastern'))
        formatted_game_time = game_time_est.strftime('%Y-%m-%d %I:%M %p %Z')

         # Determine the result emoji
        result_emoji = "✅" if selected_game['betResult'] == 'won' else "❌"

        # Construct the message based on the pickType
        if selected_game['pickType'] == 'money line':
            message = (
                f"Last 48 hours Money Line Result from {username_display}:\n"
                f"League: {league}\n"
                f"Team Picked: {selected_game['teamPicked']}\n"
                f"Odds: {selected_game['odds']}\n"
                f"Result: {selected_game['betResult']} {result_emoji}\n"
                f"Game Time: {formatted_game_time}\n\n"
                f"To track {username_display}'s success rate, check out sure-odds.com\n"
                f"#GamblingX"
            )
        elif selected_game['pickType'] == 'props':
            message = (
                f"Last 48 hours Props Result from {username_display}:\n"
                f"League: {league}\n"
                f"Player Picked: {selected_game['playerPicked']}\n"
                f"market: {market}\n"
                f"Prop Line: {selected_game['propLine']}\n"
                f"Over/Under: {selected_game['propOverOrUnder']}\n"
                f"Odds: {selected_game['odds']}\n"
                f"Result: {selected_game['betResult']} {result_emoji}\n"
                f"Game Time: {formatted_game_time}\n\n"
                f"To track {username_display}'s success rate, check out sure-odds.com\n"
                f"#GamblingX"
            )
        else:
            # No valid pick type found, do not send a message
            return

        # Ensure the message does not exceed 280 characters
        if len(message) > 280:
            message = message[:280 - len(f"To track {username_display}'s success rate, check out sure-odds.com\n#GamblingX")] + f"... To track {username_display}'s success rate, check out sure-odds.com\n#GamblingX"

        # Print the message
        print(message)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    # Authenticate with Twitter API
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    client.create_tweet(text=message)
    print("Message posted on Twitter.")

    print("Script for posting optimized message on Twitter running")

# call_sure_odds_automated_wins_loss_marketing()

# Set the Eastern Time (EST) timezone
est = pytz.timezone('US/Eastern')

# Schedule the script to run every 2 hours
schedule.every(3).hours.do(call_sure_odds_automated_wins_loss_marketing)

# # Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)