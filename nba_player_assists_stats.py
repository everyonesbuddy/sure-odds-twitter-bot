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

def nba_player_assists_stats():
    # Authenticate with Twitter API
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # OddsAPI NBA Games API endpoint and player assists stats API
    nba_games_and_odds_api_url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey=5e7c521ab26381b068424419c586233a&regions=us&markets=h2h&oddsFormat=american&bookmakers=fanduel"
    nba_player_assists_stats_url = "https://sheet.best/api/sheets/6ffde7e5-71ac-4827-b162-18ba2d90ecb9/tabs/NBA_Player_Props_Assists"

    # External API call to get odds data
    response = requests.get(nba_games_and_odds_api_url)
    odds_data = response.json()


    # Function to get NBA Player assits stats
    def get_nba_player_assists_stats(team_name):
        response = requests.get(nba_player_assists_stats_url)
        nba_player_assists_stats_data = response.json()

        for nba_player_assists_data in nba_player_assists_stats_data:
            if nba_player_assists_data["team"].lower() == team_name.lower():
                return nba_player_assists_data

        return None


    # Loop through first 3 upcoming games and Loop through NBA Player assists stats data and match the team playing with player on that team and display their stats
    for game in odds_data[:3]:
        home_team = game["home_team"]
        away_team = game["away_team"]
        commence_time_str = game['commence_time']

        # Convert UTC time to Eastern Time (EST)
        commence_time_utc = datetime.strptime(commence_time_str, "%Y-%m-%dT%H:%M:%SZ")
        est = pytz.timezone('US/Eastern')
        commence_time_est = commence_time_utc.replace(tzinfo=pytz.utc).astimezone(est)

        formatted_commence_time = commence_time_est.strftime("%a %b %d, %Y %I:%M %p %Z")

        # Check if home team's NBA Player assists data is available
        home_nba_player_assists_stats = get_nba_player_assists_stats(home_team)
        if home_nba_player_assists_stats:
            tweet_text = (
                f"🚨{home_team} Player ({home_nba_player_assists_stats['player']}) Assists:"
                f"\n Last Game: {home_nba_player_assists_stats['assistsLastGame']},"
                f"\n 2 Games Ago: {home_nba_player_assists_stats['assistsTwoGamesAgo']},"
                f"\n 3 Games Ago: {home_nba_player_assists_stats['assistsThreeGamesAgo']},"
                f"\n 4 Games Ago: {home_nba_player_assists_stats['assistsFourGamesAgo']},"
                f"\n 5 Games Ago: {home_nba_player_assists_stats['assistsFiveGamesAgo']},"
                f"\n Avg Last 3 Games: {home_nba_player_assists_stats['avergeLastThree']}"
                f"\n Szn Avg: {home_nba_player_assists_stats['assistsPerGameCurrentSeason']}"
                f"\n🏀 Next:  vs {away_team} on {formatted_commence_time}"
                f"\n🏆#GamblingTwitter"
            )
            print(tweet_text)
            client.create_tweet(text = tweet_text)
        else:
            print(f"No NBA Player assists stats found for {home_team}")

        # Check if away team's NBA Player Assists data is available
        away_nba_player_assists_stats = get_nba_player_assists_stats(away_team)
        if away_nba_player_assists_stats:
            tweet_text = (
                f"🚨{away_team} Player ({away_nba_player_assists_stats['player']}) Assists:"
                f"\n Last Game: {away_nba_player_assists_stats['assistsLastGame']},"
                f"\n 2 Games Ago: {away_nba_player_assists_stats['assistsTwoGamesAgo']},"
                f"\n 3 Games Ago: {away_nba_player_assists_stats['assistsThreeGamesAgo']},"
                f"\n 4 Games Ago: {away_nba_player_assists_stats['assistsFourGamesAgo']},"
                f"\n 5 Games Ago: {away_nba_player_assists_stats['assistsFiveGamesAgo']},"
                f"\n Avg Last 3 Games: {away_nba_player_assists_stats['avergeLastThree']}"
                f"\n Szn Avg: {away_nba_player_assists_stats['assistsPerGameCurrentSeason']}"
                f"\n🏀 Next: vs {home_team} on {formatted_commence_time}"
                f"\n🏆#GamblingTwitter"
            )
            print(tweet_text)
            client.create_tweet(text = tweet_text)
        else:
            print(f"No NBA Player assists stats found for {away_team}")

# Set the Eastern Time (EST) timezone
est = pytz.timezone('US/Eastern')

# Schedule the script to run every day at 2 PM EST
schedule.every().day.at("14:00").do(nba_player_assists_stats).timezone = est

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)