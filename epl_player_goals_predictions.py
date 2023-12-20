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

def epl_player_goals_predictions():
    # Authenticate with Twitter API
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # OddsAPI EPL Games API endpoint and EPL Soccer playee passing yards stats API
    epl_games_and_odds_api_url = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?apiKey=5e7c521ab26381b068424419c586233a&regions=us&markets=h2h&oddsFormat=american&bookmakers=fanduel"
    epl_player_goals_stats_url = "https://sheet.best/api/sheets/7d7280c1-16cf-4eaf-8cb6-f14ee6809071"

    # External API call to get odds data
    response = requests.get(epl_games_and_odds_api_url)
    odds_data = response.json()


    # Function to get EPL Player Soccer stats
    def get_epl_player_goals_stats(team_name):
        response = requests.get(epl_player_goals_stats_url)
        epl_player_goals_stats_data = response.json()

        for epl_palyer_goals_data in epl_player_goals_stats_data:
            if epl_palyer_goals_data["team"].lower() == team_name.lower():
                return epl_palyer_goals_data

        return None


    # Loop through first 3 upcoming games and Loop through EPL soccer player stats data and match the team playing with player on that team and display their stats
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
        draw_price = team_prices.get('Draw')

        # Check if home team's Epl soccer player data is available
        home_epl_players_goals_stats = get_epl_player_goals_stats(home_team)
        if home_epl_players_goals_stats:

            # Call AI API with your team and player data and then recieve response back to be posted
            ai_api_url = 'https://streamfling-be.herokuapp.com/'
            ai_prompt = f"You are a professional soccer bettor, that analyses data, and based on that data posts player prop picks/predictions on Twitter. I will provide you with some data points which include the teams playing, commence time, and historical data on a player from one of the teams playing. You will use the data points and make player prop picks/predictions based on the data points provided. This prediction post should be in a bullet point format that consists of the player prop pick, the teams playing, the commence time, the player's last 3 games average, and the player's season average as individual bulletpoints. Do Not include any data in your post that I did not provide you in the post like do not include odds on your player props projections in your post cause we do not have that data. Note do not execed a max of 280 characters on the post. Here are the data points: {home_team} vs {away_team}, {bookmaker_title} Odds - {home_team}: {home_team_price}, {away_team}, Draw: {draw_price}: {away_team_price}, Commence Time: {formatted_commence_time}. Player ({home_epl_players_goals_stats['player']}) Goals: Last Game: {home_epl_players_goals_stats['goalsLastGame']}, 2 Games Ago: {home_epl_players_goals_stats['goalsTwoGamesAgo']}, 3 Games Ago: {home_epl_players_goals_stats['goalsThreeGamesAgo']}, 4 Games Ago: {home_epl_players_goals_stats['goalsFourGamesAgo']}, 5 Games Ago: {home_epl_players_goals_stats['goalsFiveGamesAgo']}, Avg Last 3 Games: {home_epl_players_goals_stats['avergeLastThree']}, Szn Avg: {home_epl_players_goals_stats['goalsPerGameCurrentSeason']}."
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
            print(f"No Epl soccer player stats found for {home_team}")

        # Check if away team's Epl soccer player data is available
        away_epl_players_goals_stats = get_epl_player_goals_stats(away_team)
        if away_epl_players_goals_stats:

            # Call AI API with your team and player data and then recieve response back to be posted
            ai_api_url = 'https://streamfling-be.herokuapp.com/'
            ai_prompt = f"You are a professional soccer bettor, that analyses data, and based on that data posts player prop picks/predictions on Twitter. I will provide you with some data points which include the teams playing, commence time, and historical data on a player from one of the teams playing. You will use the data points and make player prop picks/predictions based on the data points provided. This prediction post should be in a bullet point format that consists of the player prop pick, the teams playing, the commence time, the player's last 3 games average, and the player's season average as individual bulletpoints. Do Not include any data in your post that I did not provide you in the post like do not include odds on your player props projections in your post cause we do not have that data. Note do not execed a max of 280 characters on the post. Here are the data points: {home_team} vs {away_team}, {bookmaker_title} Odds - {home_team}: {home_team_price}, {away_team}, Draw: {draw_price}: {away_team_price}, Commence Time: {formatted_commence_time}. Player ({away_epl_players_goals_stats['player']}) Goals: Last Game: {away_epl_players_goals_stats['goalsLastGame']}, 2 Games Ago: {away_epl_players_goals_stats['goalsTwoGamesAgo']}, 3 Games Ago: {away_epl_players_goals_stats['goalsThreeGamesAgo']}, 4 Games Ago: {away_epl_players_goals_stats['goalsFourGamesAgo']}, 5 Games Ago: {away_epl_players_goals_stats['goalsFiveGamesAgo']}, Avg Last 3 Games: {away_epl_players_goals_stats['avergeLastThree']}, Szn Avg: {away_epl_players_goals_stats['goalsPerGameCurrentSeason']}."
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
            print(f"No Epl soccer player stats found for {away_team}")


# Set the Eastern Time (EST) timezone
est = pytz.timezone('US/Eastern')

# Schedule the script to run every day at 9 AM EST
schedule.every().day.at("09:00").do(epl_player_goals_predictions).timezone = est

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)