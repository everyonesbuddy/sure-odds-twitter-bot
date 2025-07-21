import requests
import tweepy
import random
import schedule
import time
from datetime import datetime, timedelta
# import pytz

# === Twitter API Credentials ===
api_key = "F2MU6zhUDEPPcU3pOxfJq7J2Y"
api_secret = "jEBgijrY1Aigsy3bpVJldv4WFwshcr2RWFWqLhAeK5QMrKX7zJ"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAFgGrQEAAAAAcRPWLTcm5Dsd5Q%2F2cYcBSpdHnVo%3DzBRuxFGDKRBqLBr7gPzSp5qeGs5WK3dmC4va8n84FUSZSWyspR"
access_token = "1646168850147295234-Zw5P0wkecRHbXyTqXbT7JJbm264t8F"
access_token_secret = "gRK0iRZ0akKe7JQOL41xIYRJri9PtbmsTCqkmfEuDXt1V"

# === Twitter Authentication ===
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Calculate start of current Sunday (12:00 AM)
today = datetime.now()
start_of_week = today - timedelta(days=today.weekday() + 1)  # Move to Sunday
start_date = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")

# Calculate end of current Saturday (11:59 PM)
end_of_week = start_of_week + timedelta(days=6)  # Move to Saturday
end_date = end_of_week.replace(hour=23, minute=59, second=59, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")

# === Contest Configuration ===
contests = [
    {
        "title": "Weekly WNBA Streak",
        "prize": "$100",
        "duration": "weekly",
        "start_date": start_date,
        "end_date": end_date,
        "expected_streak": 5,
        "images": [
            "./wnba-streak.png",
        ]
    },
    # {
    #     "title": "Weekly MLB Streak",
    #     "prize": "$100",
    #     "duration": "weekly",
    #     "start_date": start_date,
    #     "end_date": end_date,
    #     "expected_streak": 5,
    #     "images": [
    #         "./mlb-streak.jpg",
    #     ]
    # }
]


# === Supported Leagues & Emojis ===
leagues = {
    "basketball_wnba": "WNBA Basketball",
    "baseball_mlb": "MLB Baseball"
}
emojis = {
    "basketball_wnba": "🏀",
    "baseball_mlb": "⚾"
}

# === Message Templates ===
templates = [
    "🎯 Go {streak}-for-{streak} ATS and win a {prize} {duration}!\n\n{matchups}\n\nContest starts {start_date} and ends {end_date}. Only {days_left} days left!\nMake picks. Build a streak. Win prizes. Free to play.",
    "🔥 ATS streak contest is live!\n\n{matchups}\n\nMake {streak} picks against the spread to win {prize}.\nContest ends {end_date}. Hurry, {days_left} days remaining!\nNo cost. Just your skill.",
    "🏆 Think you can go perfect ATS this {duration}?\n\n{matchups}\n\nHit a {streak}-pick streak. Free to enter. {prize} up for grabs.\nContest ends {end_date}. Only {days_left} days left!",
    "🚨 Free-to-play ATS streak challenge!\nPick {streak}. Go perfect. Win {prize} {duration}.\n\n{matchups}\n\nContest ends {end_date}. {days_left} days remaining!\nIt’s you vs. the lines.",
    "📈 {streak} picks. 1 streak. {prize} {duration}.\nNo entry fee. Just your sharp picks.\n\n{matchups}\n\nContest ends {end_date}. Hurry, {days_left} days left!"
]

# === Fetch Matchups from Odds API ===
def get_matchups(league_key, max_games=2):
    odds_url = (
        f"https://api.the-odds-api.com/v4/sports/{league_key}/odds/"
        f"?apiKey=402f2e4bba957e5e98c7e1a178393c8c"
        f"&regions=us&markets=spreads&oddsFormat=american&bookmakers=fanduel"
    )

    try:
        response = requests.get(odds_url)
        response.raise_for_status()
        games = response.json()
        if not games:
            return None

        formatted_games = []
        for game in games[:max_games]:
            home = game['home_team']
            away = game['away_team']
            outcomes = game['bookmakers'][0]['markets'][0]['outcomes']
            spreads = {o['name']: o['point'] for o in outcomes}
            prices = {o['name']: o['price'] for o in outcomes}

            home_line = f"{home} ({spreads.get(home, '?')} | {prices.get(home, '?')})"
            away_line = f"{away} ({spreads.get(away, '?')} | {prices.get(away, '?')})"
            emoji = emojis.get(league_key, "")
            league_title = leagues[league_key]

            match_str = (
                f"{emoji} {home} vs. {away} – {league_title}\n"
                f"  • {home_line}\n"
                f"  • {away_line}"
            )
            formatted_games.append(match_str)

        return "\n\n".join(formatted_games)

    except Exception as e:
        print(f"Error fetching matchups: {e}")
        return None

# === Main Tweet Function ===
def post_contest_promo():
    contest = random.choice(contests)
    league_key = random.choice(list(leagues.keys()))
    matchups = get_matchups(league_key)

    if not matchups:
        print("No matchup data available.")
        return

    # Calculate days left until contest ends
    end_date_obj = datetime.strptime(contest["end_date"], "%Y-%m-%d %H:%M:%S")
    days_left = (end_date_obj - datetime.now()).days

     # Format start_date and end_date without time
    formatted_start_date = datetime.strptime(contest["start_date"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
    formatted_end_date = end_date_obj.strftime("%Y-%m-%d")

    template = random.choice(templates)
    tweet = template.format(
        prize=contest["prize"],
        duration=contest["duration"],
        streak=contest["expected_streak"],
        matchups=matchups,
        start_date=formatted_start_date,
        end_date=formatted_end_date,
        days_left=days_left
    )

    image_path = random.choice(contest["images"])
    media = api.media_upload(image_path)

    client.create_tweet(text=tweet, media_ids=[media.media_id])
    print("Tweet posted:\n", tweet)

# Schedule Bots
# schedule.every().day.at("12:00").do(post_contest_promo)
schedule.every(6).hours.do(post_contest_promo)

while True:
    schedule.run_pending()
    time.sleep(1)

# post_contest_promo()