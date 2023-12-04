import requests
import tweepy
from datetime import datetime
import pytz
import schedule
import time

# Your Twitter API credentials
api_key = "F2MU6zhUDEPPcU3pOxfJq7J2Y"
api_secret = "jEBgijrY1Aigsy3bpVJldv4WFwshcr2RWFWqLhAeK5QMrKX7zJ"
bearer_token = r"AAAAAAAAAAAAAAAAAAAAAFgGrQEAAAAAcRPWLTcm5Dsd5Q%2F2cYcBSpdHnVo%3DzBRuxFGDKRBqLBr7gPzSp5qeGs5WK3dmC4va8n84FUSZSWyspR"
access_token = "1646168850147295234-Zw5P0wkecRHbXyTqXbT7JJbm264t8F"
access_token_secret = "gRK0iRZ0akKe7JQOL41xIYRJri9PtbmsTCqkmfEuDXt1V"

def call_nba_games_ml_odds():
    # Authenticate with Twitter API
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # OddsAPI NBA Games API endpoint
    nba_games_and_odds_api_url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey=5e7c521ab26381b068424419c586233a&regions=us&markets=h2h&oddsFormat=american&bookmakers=fanduel"

    # Make a request to the API
    response = requests.get(nba_games_and_odds_api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data
        odds_data = response.json()

        # Iterate through each game in the odds data and Limit the loop to the first 2 games
        for i, game in enumerate(odds_data[:2]):
            # Extract relevant information
            home_team = game['home_team']
            away_team = game['away_team']
            commence_time_str = game['commence_time']

            # Convert UTC time to Eastern Time (EST)
            commence_time_utc = datetime.strptime(commence_time_str, "%Y-%m-%dT%H:%M:%SZ")
            est = pytz.timezone('US/Eastern')
            commence_time_est = commence_time_utc.replace(tzinfo=pytz.utc).astimezone(est)

            formatted_commence_time = commence_time_est.strftime("%a %b %d, %Y %I:%M %p %Z")

            bookmaker = game['bookmakers'][0]['title']  # Assuming there's always at least one bookmaker
            home_team_price = game['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
            away_team_price = game['bookmakers'][0]['markets'][0]['outcomes'][1]['price']

            # Create a tweet text
            tweet_text = (
                f"🏀 {home_team} vs {away_team}\n"
                f"📅 Commence Time: {formatted_commence_time}\n"
                f"{bookmaker} Odds:\n"
                f"  {home_team} - [{home_team_price}],\n"
                f"  {away_team} - [{away_team_price}].\n"
                "#GamblingTwitter"
            )

            # Post the tweet
            # api.update_status(status=tweet_text)
            client.create_tweet(text = tweet_text)

            print(f"Tweet posted for Game {i + 1}: {tweet_text}")
    else:
        print(f"Error in API request. Status code: {response.status_code}")

# Set the Eastern Time (EST) timezone
est = pytz.timezone('US/Eastern')

# Schedule the script to run every day at 2:40 PM EST
schedule.every().day.at("14:47").do(call_nba_games_ml_odds).timezone = est

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
