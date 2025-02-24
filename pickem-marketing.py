import requests
import tweepy
import random
import schedule
import time
from datetime import datetime
import pytz

# Twitter API credentials
api_key = "F2MU6zhUDEPPcU3pOxfJq7J2Y"
api_secret = "jEBgijrY1Aigsy3bpVJldv4WFwshcr2RWFWqLhAeK5QMrKX7zJ"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAFgGrQEAAAAAcRPWLTcm5Dsd5Q%2F2cYcBSpdHnVo%3DzBRuxFGDKRBqLBr7gPzSp5qeGs5WK3dmC4va8n84FUSZSWyspR"
access_token = "1646168850147295234-Zw5P0wkecRHbXyTqXbT7JJbm264t8F"
access_token_secret = "gRK0iRZ0akKe7JQOL41xIYRJri9PtbmsTCqkmfEuDXt1V"

# Authenticate with Twitter API
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# List of PNG images
contestPromoImages = ["./contest-marketing-asset-1.png", "./contest-marketing-asset-2.png", "./contest-marketing-asset-3.png"]

# Dictionary of leagues with keys and display names
leagues = {
    "basketball_nba": "NBA Basketball",
    "soccer_epl": "English Premier League Soccer",
    "soccer_germany_bundesliga": "German Bundesliga Soccer",
    "basketball_ncaab": "NCAA Basketball",
    "soccer_italy_serie_a": "Italian Serie A Soccer",
    "soccer_spain_la_liga": "Spanish La Liga Soccer",
    "soccer_usa_mls": "USA Major League Soccer"
}

# Dictionary of sport emojis
sport_emojis = {
    "basketball_nba": "🏀",
    "soccer_epl": "⚽",
    "soccer_germany_bundesliga": "⚽",
    "basketball_ncaab": "🏀",
    "soccer_italy_serie_a": "⚽",
    "soccer_spain_la_liga": "⚽",
    "soccer_usa_mls": "⚽"
}

# Contest Series - Game Matchups & Odds Bot
def post_game_matchups():
    league_key = random.choice(list(leagues.keys()))
    league_name = leagues[league_key]
    sport_emoji = sport_emojis[league_key]

    odds_api_url = f"https://api.the-odds-api.com/v4/sports/{league_key}/odds/?apiKey=402f2e4bba957e5e98c7e1a178393c8c&regions=us&markets=h2h&oddsFormat=american&bookmakers=fanduel"
    response = requests.get(odds_api_url)

    if response.status_code == 200:
        odds_data = response.json()
        for game in odds_data[:1]:  # Limit to first 1 games
            home_team = game['home_team']
            away_team = game['away_team']

            team_prices = {outcome['name']: outcome['price'] for outcome in game['bookmakers'][0]['markets'][0]['outcomes']}
            home_team_price = team_prices.get(home_team)
            away_team_price = team_prices.get(away_team)
            draw_price = team_prices.get('Draw') if 'Draw' in team_prices else None

            if draw_price:
                message = (
                    f"🔥 **MATCHUP ALERT!** 🔥\n"
                    f"{sport_emoji} {home_team} vs. {away_team} – {league_name} Showdown!\n"
                    f"💰 **Odds:** {home_team} ({home_team_price}) | {away_team} ({away_team_price})" +
                    (f" | Draw ({draw_price})") + "\n"
                    f"📢 Who are you backing? Drop your picks below! ⬇️\n"
                    f"#SportsBetting #GameDay #BettingTips #WinCrypto"
                )
            else:
                message = (
                    f"🔥 **MATCHUP ALERT!** 🔥\n"
                    f"{sport_emoji} {home_team} vs. {away_team} – {league_name} Showdown!\n"
                    f"💰 **Odds:** {home_team} ({home_team_price}) | {away_team} ({away_team_price})"
                    f"📢 Who are you backing? Drop your picks below! ⬇️\n"
                    f"#SportsBetting #GameDay #BettingTips #WinCrypto"
                )

            # Select a random image
            image_path = random.choice(contestPromoImages)
            media = api.media_upload(image_path)
            media_id = media.media_id

            client.create_tweet(text=message, media_ids=[media_id])
            print(f"Tweeted: {message} with image {image_path}")
    else:
        print("Error fetching odds data")

# Meme & FOMO Content Bot
def sports_hypotheticals():

    assets = {
        "Who wins in a 1v1" : "./contest-marketing-asset-4.png",
        "Pick One to Hit the Game-Winner" : "./contest-marketing-asset-5.png",
    }

    asset_key = random.choice(list(assets.keys()))
    image_path = assets[asset_key]

    media = api.media_upload(image_path)
    media_id = media.media_id

    client.create_tweet(text=asset_key, media_ids=[media_id])
    print(f"Tweeted: {asset_key} with image {image_path}")

# Schedule Bots
schedule.every().day.at("10:00").do(post_game_matchups)
schedule.every(2).days.at("15:00").do(sports_hypotheticals)

while True:
    schedule.run_pending()
    time.sleep(1)


