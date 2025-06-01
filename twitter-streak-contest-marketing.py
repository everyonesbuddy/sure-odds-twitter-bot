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
    # "basketball_ncaab": "NCAA Basketball",
    "soccer_italy_serie_a": "Italian Serie A Soccer",
    "soccer_spain_la_liga": "Spanish La Liga Soccer",
    "soccer_usa_mls": "USA Major League Soccer",
    "icehockey_nhl": "NHL Ice Hockey",
}

# Dictionary of sport emojis
sport_emojis = {
    "basketball_nba": "🏀",
    "soccer_epl": "⚽",
    "soccer_germany_bundesliga": "⚽",
    # "basketball_ncaab": "🏀",
    "soccer_italy_serie_a": "⚽",
    "soccer_spain_la_liga": "⚽",
    "soccer_usa_mls": "⚽",
    "icehockey_nhl": "🏒",
}

# List of promo images
contest_promo_images = [
    "./contest-marketing-asset-1.png",
    "./contest-marketing-asset-2.png",
    "./contest-marketing-asset-3.png"
]

# Steak Contest Message Templates (with placeholders)
streak_contest_templates = [
    "💸 Most ways to profit from sports picks require betting. Not here.\n\nJust make free picks, hit a streak, and win 💰 in the {title}.\n\n🏆 {total_prize} up for grabs {duration}. No entry. No catch.",

    "📣 Tired of risking your money on bets?\n\nSkip the wagers. Make picks for FREE in the {title}.\n\n🏆 Hit a streak. Win up to {total_prize} {duration}. Real cash. No fees.",

    "🎯 Think you’re sharp at picking games?\n\nTry it risk-free.\n\nJoin the {title}. Hit a hot streak. Win {total_prize} {duration}.\n\nNo gambling. No entry fees. Just you vs the games.",

    "🤔 Why risk your money when you can earn for FREE?\n\nMake your picks in the {title}. Get hot. Win cash.\n\n💰 {total_prize} in real prizes {duration}. Free to enter. No BS.",

    "🧢 Betting without risk is finally real.\n\nJoin the {title}, go on a win streak, and win up to {total_prize} {duration}.\n\nNo entry fees. No wagers. Just you and your picks.",

    "🔥 Predict games. Build your streak. Win real money.\n\nThe {title} is 100% free to enter.\n\n💵 {total_prize} paid out {duration}.\n\nNo betting. Just skill.",
]



# Contest Options
contests = [
    {
        "title": "Weekly Streaks Contest",
        "total_prize": "$500",
        "duration": "Weekly",
    },
    {
        "title": "Monthly Streaks Contest",
        "total_prize": "$2000",
        "duration": "Monthly",
    },
]

# Function to post a grand gesture contest promo
def post_streak_contest_promo():
    selected_contest = random.choice(contests)  # Randomly select a contest
    message_template = random.choice(streak_contest_templates)  # Select a random message template

    # Format message with contest details
    message = message_template.format(
        title=selected_contest["title"],
        total_prize=selected_contest["total_prize"],
        duration=selected_contest["duration"],
    )

    image_path = random.choice(contest_promo_images)  # Select a random image

    media = api.media_upload(image_path)
    media_id = media.media_id

    # client.create_tweet(text=message, media_ids=[media_id])
    client.create_tweet(text=message)
    # print(f"Tweeted: {message} with image {image_path}")
    print(f"Tweeted: {message}")


# Contest Series - Game Matchups & Odds Bot
def post_matchday_pick():
    league_key = random.choice(list(leagues.keys()))
    league_name = leagues[league_key]
    sport_emoji = sport_emojis[league_key]

    odds_api_url = f"https://api.the-odds-api.com/v4/sports/{league_key}/odds/?apiKey=402f2e4bba957e5e98c7e1a178393c8c&regions=us&markets=h2h&oddsFormat=american&bookmakers=fanduel"
    response = requests.get(odds_api_url)

    if response.status_code == 200:
        odds_data = response.json()
        for game in odds_data[:1]:  # Limit to first 1 game
            home_team = game['home_team']
            away_team = game['away_team']
            team_prices = {outcome['name']: outcome['price'] for outcome in game['bookmakers'][0]['markets'][0]['outcomes']}

            home_team_price = team_prices.get(home_team)
            away_team_price = team_prices.get(away_team)
            draw_price = team_prices.get('Draw') if 'Draw' in team_prices else None

            # Suggest a pick (randomly between home/away or draw if available)
            pick_options = [home_team, away_team]
            if draw_price:
                pick_options.append("Draw")
            suggested_pick = random.choice(pick_options)

            # Build the message
            if draw_price:
                message = (
                    f"🔥 PREDICT & WIN 🔥\n"
                    f"{sport_emoji} {home_team} vs. {away_team} – {league_name}\n"
                    f"💰 Odds: {home_team} ({home_team_price}) | {away_team} ({away_team_price}) | Draw ({draw_price})\n\n"
                    f"Our pick: **{suggested_pick}**\n\n"
                    f"Make your own pick FREE. Hit a streak. Win real 💵.\n"
                    f"🏆 $500 weekly. No entry. No betting. Just skill.\n\n"
                )
            else:
                message = (
                    f"🔥 PREDICT & WIN 🔥\n"
                    f"{sport_emoji} {home_team} vs. {away_team} – {league_name}\n"
                    f"💰 Odds: {home_team} ({home_team_price}) | {away_team} ({away_team_price})\n\n"
                    f"Our pick: **{suggested_pick}**\n\n"
                    f"Make your own pick FREE. Hit a streak. Win real 💵.\n"
                    f"🏆 $500 weekly. No entry. No betting. Just skill.\n\n"
                )

            image_path = random.choice(contestPromoImages)
            media = api.media_upload(image_path)
            media_id = media.media_id

            client.create_tweet(text=message)
            print(f"Tweeted: {message}")
    else:
        print("Error fetching odds data")

# Schedule Bots
schedule.every().day.at("10:00").do(post_streak_contest_promo)
schedule.every().day.at("12:00").do(post_streak_contest_promo)
schedule.every(2).days.at("15:00").do(post_matchday_pick)

while True:
    schedule.run_pending()
    time.sleep(1)

