import requests
import tweepy
# from datetime import datetime
import pytz
import schedule
import time
from datetime import datetime, timedelta

# Your Twitter API credentials
api_key = "F2MU6zhUDEPPcU3pOxfJq7J2Y"
api_secret = "jEBgijrY1Aigsy3bpVJldv4WFwshcr2RWFWqLhAeK5QMrKX7zJ"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAFgGrQEAAAAAcRPWLTcm5Dsd5Q%2F2cYcBSpdHnVo%3DzBRuxFGDKRBqLBr7gPzSp5qeGs5WK3dmC4va8n84FUSZSWyspR"
access_token = "1646168850147295234-Zw5P0wkecRHbXyTqXbT7JJbm264t8F"
access_token_secret = "gRK0iRZ0akKe7JQOL41xIYRJri9PtbmsTCqkmfEuDXt1V"



def nba_sharp_money_reports():
    # Authenticate with Twitter API
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # Step 1: Get Event ID
    api_url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey=9a74934bfd1e9d98c6cc43068f53e7ae&regions=us&markets=h2h&oddsFormat=american&bookmakers=pointsbetus"
    response = requests.get(api_url)

    if response.status_code != 200:
        print(f"Error in API request. Status code: {response.status_code}")
        return

    odds_data = response.json()
    if not odds_data:
        print("No odds data available.")
        return

    event_id = odds_data[0]['id']

    # Step 2: Get Current and Previous Odds
    current_api_url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey=9a74934bfd1e9d98c6cc43068f53e7ae&regions=us&markets=h2h&oddsFormat=american&bookmakers=pointsbetus&eventIds={event_id}"
    current_response = requests.get(current_api_url)

    if current_response.status_code != 200:
        print(f"Error in API request. Status code: {current_response.status_code}")
        return

    current_odds = current_response.json()

    if not current_odds or not current_odds[0].get('bookmakers'):
        print("No odds or bookmakers available for the current event ID.")
        return

    previous_timestamp = (datetime.utcnow() - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
    previous_api_url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds-history/?apiKey=9a74934bfd1e9d98c6cc43068f53e7ae&regions=us&markets=h2h&date={previous_timestamp}&bookmakers=pointsbetus&oddsFormat=american&eventIds={event_id}"
    previous_response = requests.get(previous_api_url)

    if previous_response.status_code != 200:
        print(f"Error in API request. Status code: {previous_response.status_code}")
        return

    previous_odds = previous_response.json()

    if not previous_odds:
        print("No previous odds available for the current event ID.")
        return

   # Step 3: Calculate Line Movement
    current_team_1_price = current_odds[0]['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
    previous_team_1_price = previous_odds['data'][0]['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
    current_team_2_price = current_odds[0]['bookmakers'][0]['markets'][0]['outcomes'][1]['price']
    previous_team_2_price = previous_odds['data'][0]['bookmakers'][0]['markets'][0]['outcomes'][1]['price']

    team_1_name = current_odds[0]['bookmakers'][0]['markets'][0]['outcomes'][0]['name']
    team_2_name = current_odds[0]['bookmakers'][0]['markets'][0]['outcomes'][1]['name']

    current_time = datetime.utcnow()
    previous_time = datetime.strptime(previous_odds['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
    time_difference = (current_time - previous_time).seconds // 3600

    line_movement_percentage_home = round(((current_team_1_price - previous_team_1_price) / abs(previous_team_1_price)) * 100, 1)
    line_movement_percentage_away = round(((current_team_2_price - previous_team_2_price) / abs(previous_team_2_price)) * 100, 1)

    # Step 4: Construct Tweet
    tweet_text = (
        f"NBA Sharp Money Report\n"
        f"{team_1_name} Moneyline: Moved {line_movement_percentage_home}% from {previous_team_1_price} to {current_team_1_price} in the past {time_difference} hours.\n"
        f"{team_2_name} Moneyline: Moved {line_movement_percentage_away}% from {previous_team_2_price} to {current_team_2_price} in the past {time_difference} hours.\n"
        f"For more sharp money reports join our discord. link in bio. \n"
        f"#NBA #SharpMoney"
    )

        # Post the message on Twitter
    client.create_tweet(text=tweet_text)
    print("Message posted on Twitter.")
    print(tweet_text)

    print("Script for posting optimized message on Twitter running")


# Set the Eastern Time (EST) timezone
est = pytz.timezone('US/Eastern')

## Schedule the script to run at specific times
schedule.every().day.at("10:00").do(nba_sharp_money_reports).timezone = est
schedule.every().day.at("14:00").do(nba_sharp_money_reports).timezone = est
schedule.every().day.at("18:00").do(nba_sharp_money_reports).timezone = est

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)