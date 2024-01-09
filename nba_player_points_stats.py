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

def nba_player_points_stats():
    # Authenticate with Twitter API
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # OddsAPI NBA Games API endpoint and player points stats API
    nba_games_and_odds_api_url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey=5e7c521ab26381b068424419c586233a&regions=us&markets=h2h&oddsFormat=american&bookmakers=fanduel"
    nba_player_points_stats_url = "https://sheet.best/api/sheets/6ffde7e5-71ac-4827-b162-18ba2d90ecb9"

    # External API call to get odds data
    response = requests.get(nba_games_and_odds_api_url)
    odds_data = response.json()


    # Function to get NBA Player points stats
    def get_nba_player_points_stats(team_name):
        response = requests.get(nba_player_points_stats_url)
        nba_player_points_stats_data = response.json()

        for nba_player_points_data in nba_player_points_stats_data:
            if nba_player_points_data["team"].lower() == team_name.lower():
                return nba_player_points_data

        return None


    # Loop through first 3 upcoming games and Loop through NBA Player points stats data and match the team playing with player on that team and display their stats
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

        # Check if home team's NBA Player points data is available
        home_nba_player_points_stats = get_nba_player_points_stats(home_team)
        if home_nba_player_points_stats:

            # Call AI API with your team and player data and then recieve response back to be posted
            ai_api_url = 'https://streamfling-be.herokuapp.com/'
            ai_prompt = f"You are a professional basketball bettor, that analyses data, and based on that data posts player prop picks/predictions on Twitter. I will provide you with some data points which include the teams playing, commence time, and historical data on a player from one of the teams playing. You will use the data points and make player prop picks/predictions based on the data points provided. This prediction post should be in a bullet point format that consists of the player prop pick, the teams playing, the commence time, the player's last 3 games average, and the player's season average as individual bulletpoints. Do Not include any data in your post that I did not provide you in the post like do not include odds on your player props projections in your post cause we do not have that data. Note do not execed a max of 280 characters on the post. Here are the data points: {home_team} vs {away_team}, {bookmaker_title} Odds - {home_team}: {home_team_price}, {away_team}: {away_team_price}, Commence Time: {formatted_commence_time}. Player ({home_nba_player_points_stats['player']}) Points: Last Game: {home_nba_player_points_stats['pointsLastGame']}, 2 Games Ago: {home_nba_player_points_stats['pointsTwoGamesAgo']}, 3 Games Ago: {home_nba_player_points_stats['pointsThreeGamesAgo']}, 4 Games Ago: {home_nba_player_points_stats['pointsFourGamesAgo']}, 5 Games Ago: {home_nba_player_points_stats['pointsFiveGamesAgo']}, Avg Last 3 Games: {home_nba_player_points_stats['avergeLastThree']}, Szn Avg: {home_nba_player_points_stats['pointsPerGameCurrentSeason']}."
            ai_response = requests.post(ai_api_url, json={'prompt': ai_prompt}, headers={'Content-Type': 'application/json'})

            if ai_response.status_code == 200:
                ai_data = ai_response.json()
                ai_prediction_object = ai_data.get('bot')
                ai_prediction = ai_prediction_object.get('content')
                print(f"AI Prediction: {ai_prediction}")
                client.create_tweet(text = ai_prediction)
            else:
                print(f"Error in AI API request. Status code: {ai_response.status_code}")
        else:
            print(f"No NBA Player Points stats found for {home_team}")

        # Check if away team's NBA Player points data is available
        away_nba_player_points_stats = get_nba_player_points_stats(away_team)
        if away_nba_player_points_stats:

            # Call AI API with your team and player data and then recieve response back to be posted
            ai_api_url = 'https://streamfling-be.herokuapp.com/'
            ai_prompt = f"You are a professional basketball bettor, that analyses data, and based on that data posts player prop picks/predictions on Twitter. I will provide you with some data points which include the teams playing, commence time, and historical data on a player from one of the teams playing. You will use the data points and make player prop picks/predictions based on the data points provided. This prediction post should be in a bullet point format that consists of the player prop pick, the teams playing, the commence time, the player's last 3 games average, and the player's season average as individual bulletpoints. Do Not include any data in your post that I did not provide you in the post like do not include odds on your player props projections in your post cause we do not have that data.Note do not execed a max of 280 characters on the post. Here are the data points. Here are the data points: {home_team} vs {away_team}, {bookmaker_title} Odds - {home_team}: {home_team_price}, {away_team}: {away_team_price}, Commence Time: {formatted_commence_time}. Player ({away_nba_player_points_stats['player']}) Points: Last Game: {away_nba_player_points_stats['pointsLastGame']}, 2 Games Ago: {away_nba_player_points_stats['pointsTwoGamesAgo']}, 3 Games Ago: {away_nba_player_points_stats['pointsThreeGamesAgo']}, 4 Games Ago: {away_nba_player_points_stats['pointsFourGamesAgo']}, 5 Games Ago: {away_nba_player_points_stats['pointsFiveGamesAgo']}, Avg Last 3 Games: {away_nba_player_points_stats['avergeLastThree']}, Szn Avg: {away_nba_player_points_stats['pointsPerGameCurrentSeason']}."
            ai_response = requests.post(ai_api_url, json={'prompt': ai_prompt}, headers={'Content-Type': 'application/json'})

            if ai_response.status_code == 200:
                ai_data = ai_response.json()
                ai_prediction_object = ai_data.get('bot')
                ai_prediction = ai_prediction_object.get('content')
                print(f"AI Prediction: {ai_prediction}")
                client.create_tweet(text = ai_prediction)
            else:
                print(f"Error in AI API request. Status code: {ai_response.status_code}")
        else:
            print(f"No NBA Player Points stats found for {away_team}")

# Set the Eastern Time (EST) timezone
est = pytz.timezone('US/Eastern')

# Schedule the script to run every day at 1 PM EST
schedule.every().day.at("09:30").do(nba_player_points_stats).timezone = est

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)