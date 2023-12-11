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

def epl_player_shots_stats():
    # Authenticate with Twitter API
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # OddsAPI EPL Games API endpoint and EPL Soccer playee passing yards stats API
    epl_games_and_odds_api_url = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?apiKey=5e7c521ab26381b068424419c586233a&regions=us&markets=h2h&oddsFormat=american&bookmakers=fanduel"
    epl_player_shots_stats_url = "https://sheet.best/api/sheets/7d7280c1-16cf-4eaf-8cb6-f14ee6809071/tabs/Soccer_Player_Props_Model_Shots"

    # External API call to get odds data
    response = requests.get(epl_games_and_odds_api_url)
    odds_data = response.json()


    # Function to get EPL Player Soccer stats
    def get_epl_player_shots_stats(team_name):
        response = requests.get(epl_player_shots_stats_url)
        epl_player_shots_stats_data = response.json()

        for epl_palyer_shots_data in epl_player_shots_stats_data:
            if epl_palyer_shots_data["team"].lower() == team_name.lower():
                return epl_palyer_shots_data

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

        # Check if home team's Epl soccer player data is available
        home_epl_players_shots_stats = get_epl_player_shots_stats(home_team)
        if home_epl_players_shots_stats:
            tweet_text = (
                f"🚨{home_team} Player ({home_epl_players_shots_stats['player']}) shots:"
                f"\n Last Game: {home_epl_players_shots_stats['shotsLastGame']},"
                f"\n 2 Games Ago: {home_epl_players_shots_stats['shotsTwoGamesAgo']},"
                f"\n 3 Games Ago: {home_epl_players_shots_stats['shotsThreeGamesAgo']},"
                f"\n 4 Games Ago: {home_epl_players_shots_stats['shotsFourGamesAgo']},"
                f"\n 5 Games Ago: {home_epl_players_shots_stats['shotsFiveGamesAgo']},"
                f"\n Avg Last 3 Games: {home_epl_players_shots_stats['avergeLastThree']}"
                f"\n Szn Avg: {home_epl_players_shots_stats['shotsPerGameCurrentSeason']}"
                f"\n⚽ Next:  vs {away_team} on {formatted_commence_time}"
                f"\n#SportsBetting"
            )
            print(tweet_text)
            client.create_tweet(text = tweet_text)
        else:
            print(f"No Epl soccer player stats found for {home_team}")

        # Check if away team's Epl soccer player data is available
        away_epl_players_shots_stats = get_epl_player_shots_stats(away_team)
        if away_epl_players_shots_stats:
            tweet_text = (
                f"🚨{away_team} Player ({away_epl_players_shots_stats['player']}) shots:"
                f"\n Last Game: {away_epl_players_shots_stats['shotsLastGame']},"
                f"\n 2 Games Ago: {away_epl_players_shots_stats['shotsTwoGamesAgo']},"
                f"\n 3 Games Ago: {away_epl_players_shots_stats['shotsThreeGamesAgo']},"
                f"\n 4 Games Ago: {away_epl_players_shots_stats['shotsFourGamesAgo']},"
                f"\n 5 Games Ago: {away_epl_players_shots_stats['shotsFiveGamesAgo']},"
                f"\n Avg Last 3 Games: {away_epl_players_shots_stats['avergeLastThree']}"
                f"\n Szn Avg: {away_epl_players_shots_stats['shotsPerGameCurrentSeason']}"
                f"\n⚽ Next: vs {home_team} on {formatted_commence_time}"
                f"\n#SportsBetting"
            )
            print(tweet_text)
            client.create_tweet(text = tweet_text)
        else:
            print(f"No Epl soccer player stats found for {away_team}")


# Set the Eastern Time (EST) timezone
est = pytz.timezone('US/Eastern')

# Schedule the script to run every day at 11 AM EST
schedule.every().day.at("11:00").do(epl_player_shots_stats).timezone = est

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)