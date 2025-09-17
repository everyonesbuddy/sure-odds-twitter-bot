import tweepy
import random
import schedule
import time
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# === Twitter API Credentials (from .env) ===
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# === Odds API Key ===
odds_api_key = os.getenv("ODDS_API_KEY")

# === Supported Leagues ===
leagues = {
    "soccer_epl": "English Premier League ⚽",
    "basketball_wnba": "WNBA 🏀",
    "americanfootball_nfl": "NFL 🏈",
    "baseball_mlb": "MLB ⚾",
    "icehockey_nhl": "NHL 🏒",
    "soccer_spain_la_liga": "La Liga ⚽"
}

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

# === Date Calculations ===
today = datetime.now()
start_of_week = today - timedelta(days=today.weekday() + 1)  # Sunday
end_of_week = start_of_week + timedelta(days=6)  # Saturday
start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
next_month = start_of_month.replace(day=28) + timedelta(days=4)
end_of_month = next_month - timedelta(days=next_month.day)
end_of_month = end_of_month.replace(hour=23, minute=59, second=59, microsecond=0)

start_of_week_str = start_of_week.strftime("%Y-%m-%d %H:%M:%S")
end_of_week_str = end_of_week.strftime("%Y-%m-%d %H:%M:%S")
start_of_month_str = start_of_month.strftime("%Y-%m-%d %H:%M:%S")
end_of_month_str = end_of_month.strftime("%Y-%m-%d %H:%M:%S")

# === Contest Configuration ===
contests = [
    {
        "title": "Weekly Multi Sport Streak",
        "prize": "$100 Amazon Gift Card",
        "duration": "weekly",
        "start_date": start_of_week_str,
        "end_date": end_of_week_str,
        "contest_format": "streak",
        "win_conditions": "Hit 6 correct picks in a row",
        "entry_fee": 0,
        "images": ["./assets/weekly-multi-sport-streak-poster.png"]
    },
    {
        "title": "Season Long EPL Pickem",
        "prize": "$1000 cash prize",
        "duration": "weekly",
        "start_date": "2025-08-15 00:00:00",
        "end_date": "2026-05-24 23:59:59",
        "contest_format": "pickem",
        "win_conditions": "Have the most correct picks this EPL season",
        "entry_fee": 4.99,
        "images": ["./assets/epl-season-long-contest.png"]
    },
    {
        "title": "Monthly Multi Sport Streak",
        "prize": "$300 Amazon Gift Card",
        "duration": "monthly",
        "start_date": start_of_month_str,
        "end_date": end_of_month_str,
        "contest_format": "streak",
        "win_conditions": "Hit 12 correct picks in a row",
        "entry_fee": 0,
        "images": ["./assets/monthly-multi-sport-streak-poster.png"]
    }
]

# === Message Templates ===
templates = {
    "streak": [
        "🎯 {win_conditions} in our {title} and win {prize}!\n{entry_text}. Contest runs {start_date} to {end_date}. Only {days_left} days left to join!",
        "🔥 {title} is live! {win_conditions}. {entry_text}!\nContest ends {end_date}. {days_left} days left — join now!",
        "🏆 Can you achieve it? {win_conditions} in this {duration} streak contest.\nWin {prize}. {entry_text}. Contest closes {end_date}."
    ],
    "pickem": [
        "🎯 {win_conditions} in our {title} and win {prize}!\n{entry_text}. Contest runs {start_date} to {end_date}. Only {days_left} days left to join!",
        "🔥 {title} is live! {win_conditions}. {entry_text}!\nContest ends {end_date}. {days_left} days remaining — don’t miss out!",
        "🏆 Be the top predictor! {win_conditions} in this {duration} Pick'em.\nWin {prize}. {entry_text}. Contest closes {end_date}."
    ]
}


# === Trivia, Polls, Fun Facts, Betting Tips ===
trivia_questions = [
    {
        "question": "Who holds the record for the most goals in FIFA World Cup history?",
        "options": ["Miroslav Klose", "Ronaldo Nazário", "Lionel Messi", "Pele"],
        "answer": "Miroslav Klose"
    },
    {
        "question": "Which NFL team has won the most Super Bowls?",
        "options": ["Patriots", "Steelers", "Cowboys", "49ers"],
        "answer": "Patriots & Steelers (tied at 6)"
    },
    {
        "question": "Which MLB player holds the record for most career home runs?",
        "options": ["Barry Bonds", "Hank Aaron", "Babe Ruth", "Alex Rodriguez"],
        "answer": "Barry Bonds"
    },
    {
        "question": "Who has the most Grand Slam titles in men’s tennis?",
        "options": ["Rafael Nadal", "Novak Djokovic", "Roger Federer", "Pete Sampras"],
        "answer": "Novak Djokovic"
    },
    {
        "question": "Which NBA team has the most championships?",
        "options": ["Celtics", "Lakers", "Warriors", "Bulls"],
        "answer": "Celtics & Lakers (tied at 17)"
    },
    {
        "question": "Which country hosted the first FIFA World Cup in 1930?",
        "options": ["Brazil", "Uruguay", "Italy", "Argentina"],
        "answer": "Uruguay"
    },
    {
        "question": "Who is the only athlete to play in both a Super Bowl and a World Series?",
        "options": ["Bo Jackson", "Deion Sanders", "Brian Jordan", "Tim Tebow"],
        "answer": "Deion Sanders"
    },
    {
        "question": "What’s the maximum possible break in snooker?",
        "options": ["147", "155", "150", "160"],
        "answer": "147"
    },
    {
        "question": "Which team won the first ever Premier League title (1992/93)?",
        "options": ["Arsenal", "Liverpool", "Manchester United", "Leeds"],
        "answer": "Manchester United"
    },
    {
        "question": "Which NHL team has the most Stanley Cup wins?",
        "options": ["Toronto Maple Leafs", "Montreal Canadiens", "Detroit Red Wings", "Chicago Blackhawks"],
        "answer": "Montreal Canadiens"
    }
]


fun_facts = [
    "💡 The Super Bowl is the most-watched sporting event in the US every year.",
    "💡 Michael Phelps has more Olympic gold medals than 161 countries.",
    "💡 The fastest red card in soccer history happened just 2 seconds into a game.",
    "💡 In 1994, a baseball game was canceled because players went on strike — fans showed up anyway.",
    "💡 The longest tennis match lasted 11 hours and 5 minutes at Wimbledon 2010.",
    "💡 Wayne Gretzky has more career assists than any other NHL player has total points.",
    "💡 Wilt Chamberlain once scored 100 points in a single NBA game.",
    "💡 The Boston Celtics and Los Angeles Lakers have won nearly half of all NBA titles combined.",
    "💡 In baseball, the Chicago Cubs went 108 years without a World Series win (until 2016).",
    "💡 Brazil is the only country to qualify for every FIFA World Cup."
]

betting_tips = [
    "✅ Home underdogs often provide great value, especially in rivalry games.",
    "✅ Betting with your heart is risky — always research stats, not just favorite teams.",
    "✅ In soccer, draws happen more often than you think — don’t ignore that option.",
    "✅ Public favorites are usually overpriced — value often lies with the underdog.",
    "✅ Always compare odds across sportsbooks — a small difference can mean big payouts.",
    "✅ In NBA, back-to-back games often favor the rested team.",
    "✅ In NFL, divisional games are historically tighter than expected spreads.",
    "✅ In MLB, starting pitchers can drastically change game odds — check lineups.",
    "✅ Avoid parlays if you’re chasing consistency — focus on straight bets.",
    "✅ Bankroll management is key: never bet more than 1–5% of your bankroll on a single pick."
]

# === Contest Posting ===
def post_contest_promo():
    contest = random.choice(contests)
    start_date_obj = datetime.strptime(contest["start_date"], "%Y-%m-%d %H:%M:%S")
    end_date_obj = datetime.strptime(contest["end_date"], "%Y-%m-%d %H:%M:%S")
    days_left = (end_date_obj - datetime.now()).days

    # Build entry text
    entry_text = "FREE entry" if contest["entry_fee"] == 0 else f"Entry Fee: ${contest['entry_fee']}"

    template = random.choice(templates.get(contest["contest_format"], templates["streak"]))
    tweet = template.format(
        title=contest["title"],
        prize=contest["prize"],
        duration=contest["duration"],
        win_conditions=contest["win_conditions"],
        start_date=start_date_obj.strftime("%Y-%m-%d"),
        end_date=end_date_obj.strftime("%Y-%m-%d"),
        days_left=days_left,
        entry_text=entry_text
    )

    image_path = random.choice(contest["images"])
    media = api.media_upload(image_path)
    client.create_tweet(text=tweet, media_ids=[media.media_id])
    print("Contest tweet posted:\n", tweet)

# === Featured Matchup ===
def get_featured_matchup_moneyline():
    league_key = random.choice(list(leagues.keys()))
    league_name = leagues[league_key]
    try:
        url = f"https://api.the-odds-api.com/v4/sports/{league_key}/odds/?apiKey={odds_api_key}&regions=us&markets=h2h&oddsFormat=american&bookmakers=draftkings"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        games = res.json()
        if not games: return None, f"No matchups today for {league_name}"
        game = random.choice(games)
        home, away = game["home_team"], game["away_team"]
        outcomes = game["bookmakers"][0]["markets"][0]["outcomes"]
        moneylines = {o["name"]: o["price"] for o in outcomes}
        options = [home, away] if "Draw" not in moneylines else [home, "Draw", away]
        odds_text = f"- {home}: {moneylines.get(home,'?')}\n"
        if "Draw" in moneylines: odds_text += f"- Draw: {moneylines['Draw']}\n"
        odds_text += f"- {away}: {moneylines.get(away,'?')}"
        text = f"⚔️ Featured Matchup – {league_name}\n{home} vs {away}\n💵 Moneyline Odds:\n{odds_text}\nWho you got? Vote below! 👀"
        return text, options
    except Exception as e:
        return f"⚠️ Could not fetch matchup: {e}", None

def post_daily_matchup():
    text, options = get_featured_matchup_moneyline()
    if options:
        client.create_tweet(text=text, poll_options=options, poll_duration_minutes=1440)
    else:
        client.create_tweet(text=text)
    print("Matchup tweet posted:\n", text)

# === Trivia Poll ===
def post_trivia_question():
    trivia = random.choice(trivia_questions)
    client.create_tweet(text=f"🧠 Trivia Time!\n{trivia['question']}", poll_options=trivia['options'], poll_duration_minutes=720)
    print("Trivia poll posted:\n", trivia['question'])

# === Fun Fact or Tip ===
def post_fun_fact_or_tip():
    fact = random.choice(fun_facts + betting_tips)
    client.create_tweet(text=fact)
    print("Fact/Tip tweet posted:\n", fact)

# === Schedule All ===
schedule.every().day.at("10:00").do(post_daily_matchup)
schedule.every().day.at("12:00").do(post_contest_promo)
schedule.every().day.at("15:00").do(post_trivia_question)
schedule.every().day.at("18:00").do(post_fun_fact_or_tip)

# === Run Bot ===
while True:
    schedule.run_pending()
    time.sleep(1)

