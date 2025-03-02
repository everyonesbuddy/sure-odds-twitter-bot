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

# List of promo images
contest_promo_images = [
    "./contest-marketing-asset-1.png",
    "./contest-marketing-asset-2.png",
    "./contest-marketing-asset-3.png"
]

# Grand Gesture Message Templates (with placeholders)
grand_gesture_templates = [
    "🚨 {title} IS LIVE! 🚨\n\n🔥 {total_prize} in prizes! 🔥\nPredict sports for FREE and win BIG 💰\n\nOnly {days_left} days left! ⏳\nSign up now! 👇",
    "🏆 {title} is here! 🏆\n\n💸 Win your share of {total_prize}! 💸\n\nPredict the right picks for FREE and walk away with real crypto prizes!\n\n⏳ {days_left} days remaining!\nAre you in? 👇",
    "🔥 Who wants {total_prize}? 🔥\n\nJoin {title} for a shot at HUGE winnings!\n\n💰 It's 100% FREE to enter 💰\nBut hurry—only {days_left} days left! 🕒\n\nWhat’s stopping you? 👇",
    "🚀 Your chance to win {total_prize}! 🚀\n\nEnter {title} – the ultimate sports prediction contest.\n\n✅ No risk, no fees, just pure winnings! 💰\n⏳ Only {days_left} days left!\n\nWho’s taking home the cash? 👇"
]

# Contest Options
contests = [
    {
        "title": "March Madness Pick'em",
        "total_prize": "$500",
        "end_date": "2025-03-31",
    },
    # {
    #     "title": "NBA Playoffs Pick'em",
    #     "total_prize": "$5,000",
    #     "end_date": "2025-06-30",
    # },
    # {
    #     "title": "NFL Season Pick'em",
    #     "total_prize": "$20,000",
    #     "end_date": "2025-02-28",
    # },
    # {
    #     "title": "Soccer World Cup Pick'em",
    #     "total_prize": "$15,000",
    #     "end_date": "2025-12-31",
    # }
]

# Function to calculate days left
def calculate_days_left(end_date):
    today = datetime.today().date()
    contest_end = datetime.strptime(end_date, "%Y-%m-%d").date()
    days_left = (contest_end - today).days
    return days_left

# Function to post a grand gesture contest promo
def post_grand_gesture_promo():
    selected_contest = random.choice(contests)  # Randomly select a contest
    message_template = random.choice(grand_gesture_templates)  # Select a random message template

    # Calculate days left
    days_left = calculate_days_left(selected_contest["end_date"])

    # Format message with contest details
    message = message_template.format(
        title=selected_contest["title"],
        total_prize=selected_contest["total_prize"],
        days_left=days_left
    )

    image_path = random.choice(contest_promo_images)  # Select a random image

    media = api.media_upload(image_path)
    media_id = media.media_id

    # client.create_tweet(text=message, media_ids=[media_id])
    client.create_tweet(text=message)
    # print(f"Tweeted: {message} with image {image_path}")
    print(f"Tweeted: {message}")


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

# Schedule Bots
schedule.every().day.at("10:00").do(post_grand_gesture_promo)
# schedule.every(2).days.at("15:00").do(post_game_matchups)

while True:
    schedule.run_pending()
    time.sleep(1)

