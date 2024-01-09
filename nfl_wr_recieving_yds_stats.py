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

def nfl_wr_recieving_yds_stats():
    # Authenticate with Twitter API
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # OddsAPI NFL Games API endpoint and wr(wide reciever) passing yards stats API
    nfl_games_and_odds_api_url = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey=5e7c521ab26381b068424419c586233a&regions=us&markets=h2h&oddsFormat=american&bookmakers=fanduel"
    wr_recieving_yds_stats_url = "https://sheet.best/api/sheets/8ef04191-2224-49ad-835d-0dae6d5311d9"

    # External API call to get odds data
    response = requests.get(nfl_games_and_odds_api_url)
    odds_data = response.json()


    # Function to get WR(wide reciever) stats
    def get_wr_stats(team_name):
        response = requests.get(wr_recieving_yds_stats_url)
        wr_stats_data = response.json()

        for wr_data in wr_stats_data:
            if wr_data["team"].lower() == team_name.lower():
                return wr_data

        return None


    # Loop through first 3 upcoming games and Loop through WR stats data and match the team playing with quaterback on that team and display their stats
    for game in odds_data[:3]:
        home_team = game["home_team"]
        away_team = game["away_team"]
        commence_time_str = game['commence_time']

        # Convert UTC time to Eastern Time (EST)
        commence_time_utc = datetime.strptime(commence_time_str, "%Y-%m-%dT%H:%M:%SZ")
        est = pytz.timezone('US/Eastern')
        commence_time_est = commence_time_utc.replace(tzinfo=pytz.utc).astimezone(est)

        formatted_commence_time = commence_time_est.strftime("%a %b %d, %Y %I:%M %p %Z")

        # Check if home team's WR data is available
        home_wr_stats = get_wr_stats(home_team)
        if home_wr_stats:
            tweet_text = (
                f"🚨{home_team} WR ({home_wr_stats['player']}) Recieving Yds:"
                f"\n Last Game: {home_wr_stats['receivingYardsLastGame']},"
                f"\n 2 Games Ago: {home_wr_stats['receivingYardsTwoGamesAgo']},"
                f"\n 3 Games Ago: {home_wr_stats['receivingYardsThreeGamesAgo']},"
                f"\n 4 Games Ago: {home_wr_stats['receivingYardsFourGamesAgo']},"
                f"\n 5 Games Ago: {home_wr_stats['receivingYardsFiveGamesAgo']},"
                f"\n Avg Last 2 Games: {home_wr_stats['averageLastTwo']}"
                f"\n Szn Avg: {home_wr_stats['receivingYardsPerGameCurrentSeason']}"
                f"\n🏈 Next: vs {away_team} on {formatted_commence_time}"
                f"\n🏆#GamblingTwitter"
            )
            print(tweet_text)
            client.create_tweet(text = tweet_text)
        else:
            print(f"No WR stats found for {home_team}")

        # Check if away team's WR data is available
        away_wr_stats = get_wr_stats(away_team)
        if away_wr_stats:
            tweet_text = (
                f"🚨{away_team} WR ({away_wr_stats['player']}) Recieving Yds:"
                f"\n Last Game: {away_wr_stats['receivingYardsLastGame']},"
                f"\n 2 Games Ago: {away_wr_stats['receivingYardsTwoGamesAgo']},"
                f"\n 3 Games Ago: {away_wr_stats['receivingYardsThreeGamesAgo']},"
                f"\n 4 Games Ago: {away_wr_stats['receivingYardsFourGamesAgo']},"
                f"\n 5 Games Ago: {away_wr_stats['receivingYardsFiveGamesAgo']},"
                f"\n Avg Last 2 Games: {away_wr_stats['averageLastTwo']}"
                f"\n Szn Avg: {away_wr_stats['receivingYardsPerGameCurrentSeason']}"
                f"\n🏈 Next: vs {home_team} on {formatted_commence_time}"
                f"\n🏆#GamblingTwitter"
            )
            print(tweet_text)
            client.create_tweet(text = tweet_text)
        else:
            print(f"No WR stats found for {away_team}")

# Set the Eastern Time (EST) timezone
est = pytz.timezone('US/Eastern')

# Schedule the script to run every day at 12 PM EST
schedule.every().day.at("12:00").do(nfl_wr_recieving_yds_stats).timezone = est

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)