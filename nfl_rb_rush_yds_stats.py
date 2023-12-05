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

def nfl_rb_rush_yds_stats():
    # Authenticate with Twitter API
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # OddsAPI NFL Games API endpoint and RB(running back) passing yards stats API
    nfl_games_and_odds_api_url = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey=5e7c521ab26381b068424419c586233a&regions=us&markets=h2h&oddsFormat=american&bookmakers=fanduel"
    rb_rush_yds_stats_url = "https://sheet.best/api/sheets/519389cc-9e43-457b-8aee-9bd8c1f8d975"

    # External API call to get odds data
    response = requests.get(nfl_games_and_odds_api_url)
    odds_data = response.json()


    # Function to get RB(running back) stats
    def get_rb_stats(team_name):
        response = requests.get(rb_rush_yds_stats_url)
        rb_stats_data = response.json()

        for rb_data in rb_stats_data:
            if rb_data["team"].lower() == team_name.lower():
                return rb_data

        return None


    # Loop through first 3 upcoming games and Loop through RB stats data and match the team playing with quaterback on that team and display their stats
    for game in odds_data[:3]:
        home_team = game["home_team"]
        away_team = game["away_team"]
        commence_time_str = game['commence_time']

        # Convert UTC time to Eastern Time (EST)
        commence_time_utc = datetime.strptime(commence_time_str, "%Y-%m-%dT%H:%M:%SZ")
        est = pytz.timezone('US/Eastern')
        commence_time_est = commence_time_utc.replace(tzinfo=pytz.utc).astimezone(est)

        formatted_commence_time = commence_time_est.strftime("%a %b %d, %Y %I:%M %p %Z")

        # Check if home team's RB data is available
        home_rb_stats = get_rb_stats(home_team)
        if home_rb_stats:
            tweet_text = (
                f"🚨{home_team} RB ({home_rb_stats['player']}) Rushing Yds:"
                f"\n Last Game: {home_rb_stats['rushingYardsLastGame']},"
                f"\n 2 Games Ago: {home_rb_stats['rushingYardsTwoGamesAgo']},"
                f"\n 3 Games Ago: {home_rb_stats['rushingYardsThreeGamesAgo']},"
                f"\n 4 Games Ago: {home_rb_stats['rushingYardsFourGamesAgo']},"
                f"\n 5 Games Ago: {home_rb_stats['rushingYardsFiveGamesAgo']},"
                f"\n Avg Last 2 Games: {home_rb_stats['averageLastTwo']}"
                f"\n Szn Avg: {home_rb_stats['rushingYardsPerGameCurrentSeason']}"
                f"\n🏈 Next: vs {away_team} on {formatted_commence_time}"
                f"\n🏆#GamblingTwitter"
            )
            print(tweet_text)
            client.create_tweet(text = tweet_text)
        else:
            print(f"No RB stats found for {home_team}")

        # Check if away team's RB data is available
        away_rb_stats = get_rb_stats(away_team)
        if away_rb_stats:
            tweet_text = (
                f"🚨{away_team} RB ({away_rb_stats['player']}) Rushing Yds:"
                f"\n Last Game: {away_rb_stats['rushingYardsLastGame']},"
                f"\n 2 Games Ago: {away_rb_stats['rushingYardsTwoGamesAgo']},"
                f"\n 3 Games Ago: {away_rb_stats['rushingYardsThreeGamesAgo']},"
                f"\n 4 Games Ago: {away_rb_stats['rushingYardsFourGamesAgo']},"
                f"\n 5 Games Ago: {away_rb_stats['rushingYardsFiveGamesAgo']},"
                f"\n Avg Last 2 Games: {away_rb_stats['averageLastTwo']}"
                f"\n Szn Avg: {away_rb_stats['rushingYardsPerGameCurrentSeason']}"
                f"\n🏈 Next: vs {home_team} on {formatted_commence_time}"
                f"\n🏆#GamblingTwitter"
            )
            print(tweet_text)
            client.create_tweet(text = tweet_text)
        else:
            print(f"No RB stats found for {away_team}")

# Set the Eastern Time (EST) timezone
est = pytz.timezone('US/Eastern')

# Schedule the script to run every day at 11 AM EST
schedule.every().day.at("11:00").do(nfl_rb_rush_yds_stats).timezone = est

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
