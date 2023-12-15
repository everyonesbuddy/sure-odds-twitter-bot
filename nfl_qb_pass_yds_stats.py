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

# def nfl_qb_pass_yds_stats():
# Authenticate with Twitter API
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# OddsAPI NFL Games API endpoint and qb passing yards stats API
nfl_games_and_odds_api_url = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey=5e7c521ab26381b068424419c586233a&regions=us&markets=h2h&oddsFormat=american&bookmakers=fanduel"
qb_pass_yds_stats_url = "https://sheet.best/api/sheets/5723d7f8-f232-453d-8b48-63fbf8dc7dca"

# External API call to get odds data
response = requests.get(nfl_games_and_odds_api_url)
odds_data = response.json()


# Function to get QB stats
def get_qb_stats(team_name):
    response = requests.get(qb_pass_yds_stats_url)
    qb_stats_data = response.json()

    for qb_data in qb_stats_data:
        if qb_data["team"].lower() == team_name.lower():
            return qb_data

    return None


# Loop through first 3 upcoming games and Loop through QB stats data and match the team playing with quaterback on that team and display their stats
for game in odds_data[:3]:
    home_team = game["home_team"]
    away_team = game["away_team"]
    commence_time_str = game['commence_time']

    # Convert UTC time to Eastern Time (EST)
    commence_time_utc = datetime.strptime(commence_time_str, "%Y-%m-%dT%H:%M:%SZ")
    est = pytz.timezone('US/Eastern')
    commence_time_est = commence_time_utc.replace(tzinfo=pytz.utc).astimezone(est)

    formatted_commence_time = commence_time_est.strftime("%a %b %d, %Y %I:%M %p %Z")

    # Extract bookmaker information
    bookmaker_info = game['bookmakers'][0]
    bookmaker_title = bookmaker_info['title']

    # Create a dictionary to map team names to their prices
    team_prices = {outcome['name']: outcome['price'] for outcome in bookmaker_info['markets'][0]['outcomes']}

    # Extract prices using team names
    home_team_price = team_prices.get(home_team)
    away_team_price = team_prices.get(away_team)

    # Check if home team's QB data is available
    home_qb_stats = get_qb_stats(home_team)
    if home_qb_stats:
        # Post data to AI API
        ai_api_url = 'https://streamfling-be.herokuapp.com/'
        ai_prompt = f"You are a american football handicapper, i will provide you with some data, and you make picks also format the picks for twitter: {home_team} vs {away_team}, {bookmaker_title} Odds - {home_team}: {home_team_price}, {away_team}: {away_team_price}. Player ({home_qb_stats['player']}) Points: Last Game: {home_qb_stats['passingYardsLastGame']}, 2 Games Ago: {home_qb_stats['passingYardsTwoGamesAgo']}, 3 Games Ago: {home_qb_stats['passingYardsThreeGamesAgo']}, 4 Games Ago: {home_qb_stats['passingYardsFourGamesAgo']}, 5 Games Ago: {home_qb_stats['passingYardsFiveGamesAgo']}, Avg Last 2 Games: {home_qb_stats['averageLastTwo']}, Szn Avg: {home_qb_stats['passingYardsPerGameCurrentSeason']}."
        ai_response = requests.post(ai_api_url, json={'prompt': ai_prompt}, headers={'Content-Type': 'application/json'})

        if ai_response.status_code == 200:
            ai_data = ai_response.json()
            ai_prediction = ai_data.get('bot')
            print(f"AI Prediction: {ai_prediction}")
        else:
            print(f"Error in AI API request. Status code: {ai_response.status_code}")
        # tweet_text = (
        #     f"🚨{home_team} QB ({home_qb_stats['player']}) Passing Yds:"
        #     f"\n Last Game: {home_qb_stats['passingYardsLastGame']},"
        #     f"\n 2 Games Ago: {home_qb_stats['passingYardsTwoGamesAgo']},"
        #     f"\n 3 Games Ago: {home_qb_stats['passingYardsThreeGamesAgo']},"
        #     f"\n 4 Games Ago: {home_qb_stats['passingYardsFourGamesAgo']},"
        #     f"\n 5 Games Ago: {home_qb_stats['passingYardsFiveGamesAgo']},"
        #     f"\n Avg Last 2 Games: {home_qb_stats['averageLastTwo']}"
        #     f"\n Szn Avg: {home_qb_stats['passingYardsPerGameCurrentSeason']}"
        #     f"\n🏈 Next:  vs {away_team} on {formatted_commence_time}"
        #     f"\n🏆#GamblingTwitter"
        # )
        # print(tweet_text)
        # client.create_tweet(text = tweet_text)
    else:
        # print(f"No QB stats found for {home_team}")
        # Post data to AI API
        ai_api_url = 'https://streamfling-be.herokuapp.com/'
        ai_prompt = f"You are a american football, i will provide you with some data, and you make picks also format the picks for twitter: {home_team} vs {away_team}, {bookmaker_title} Odds - {home_team}: {home_team_price}, {away_team}: {away_team_price}."
        ai_response = requests.post(ai_api_url, json={'prompt': ai_prompt}, headers={'Content-Type': 'application/json'})

        if ai_response.status_code == 200:
            ai_data = ai_response.json()
            ai_prediction = ai_data.get('bot')
            print(f"AI Prediction: {ai_prediction}")
        else:
            print(f"Error in AI API request. Status code: {ai_response.status_code}")

    # Check if away team's QB data is available
    away_qb_stats = get_qb_stats(away_team)
    if away_qb_stats:
        # Post data to AI API
        ai_api_url = 'https://streamfling-be.herokuapp.com/'
        ai_prompt = f"You are a american football, i will provide you with some data, and you make picks also format the picks for twitter: {home_team} vs {away_team}, {bookmaker_title} Odds - {home_team}: {home_team_price}, {away_team}: {away_team_price}. Player ({away_qb_stats['player']}) Points: Last Game: {away_qb_stats['passingYardsLastGame']}, 2 Games Ago: {away_qb_stats['passingYardsTwoGamesAgo']}, 3 Games Ago: {away_qb_stats['passingYardsThreeGamesAgo']}, 4 Games Ago: {away_qb_stats['passingYardsFourGamesAgo']}, 5 Games Ago: {away_qb_stats['passingYardsFiveGamesAgo']}, Avg Last 2 Games: {away_qb_stats['averageLastTwo']}, Szn Avg: {away_qb_stats['passingYardsPerGameCurrentSeason']}."
        ai_response = requests.post(ai_api_url, json={'prompt': ai_prompt}, headers={'Content-Type': 'application/json'})

        if ai_response.status_code == 200:
            ai_data = ai_response.json()
            ai_prediction = ai_data.get('bot')
            print(f"AI Prediction: {ai_prediction}")
        else:
            print(f"Error in AI API request. Status code: {ai_response.status_code}")
        # tweet_text = (
        #     f"🚨{away_team} QB ({away_qb_stats['player']}) Passing Yds:"
        #     f"\n Last Game: {away_qb_stats['passingYardsLastGame']},"
        #     f"\n 2 Games Ago: {away_qb_stats['passingYardsTwoGamesAgo']},"
        #     f"\n 3 Games Ago: {away_qb_stats['passingYardsThreeGamesAgo']},"
        #     f"\n 4 Games Ago: {away_qb_stats['passingYardsFourGamesAgo']},"
        #     f"\n 5 Games Ago: {away_qb_stats['passingYardsFiveGamesAgo']},"
        #     f"\n Avg Last 2 Games: {away_qb_stats['averageLastTwo']}"
        #     f"\n Szn Avg: {away_qb_stats['passingYardsPerGameCurrentSeason']}"
        #     f"\n🏈 Next: vs {home_team} on {formatted_commence_time}"
        #     f"\n🏆#GamblingTwitter"
        # )
        # print(tweet_text)
        # client.create_tweet(text = tweet_text)
    else:
        # print(f"No QB stats found for {away_team}")
        # Post data to AI API
        ai_api_url = 'https://streamfling-be.herokuapp.com/'
        ai_prompt = f"You are a American football handicapper, i will provide you with some data, and you make picks also format the picks for twitter: {home_team} vs {away_team}, {bookmaker_title} Odds - {home_team}: {home_team_price}, {away_team}: {away_team_price}."
        ai_response = requests.post(ai_api_url, json={'prompt': ai_prompt}, headers={'Content-Type': 'application/json'})

        if ai_response.status_code == 200:
            ai_data = ai_response.json()
            ai_prediction = ai_data.get('bot')
            print(f"AI Prediction: {ai_prediction}")
        else:
            print(f"Error in AI API request. Status code: {ai_response.status_code}")


# Set the Eastern Time (EST) timezone
# est = pytz.timezone('US/Eastern')

# Schedule the script to run every day at 10 AM EST
# schedule.every().day.at("10:00").do(nfl_qb_pass_yds_stats).timezone = est

# Keep the script running
# while True:
#     schedule.run_pending()
#     time.sleep(1)