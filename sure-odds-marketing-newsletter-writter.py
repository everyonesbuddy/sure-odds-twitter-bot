import requests
import random
import schedule
import time
from datetime import datetime, timedelta
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Configs
SCOPES = ['https://www.googleapis.com/auth/documents']
DOCUMENT_TITLE = "Sure-Odds Daily Newsletter"

# Leagues & Emojis
leagues = {
    "basketball_wnba": "WNBA Basketball",
}

sport_emojis = {
    "basketball_wnba": "🏀",
}

# === Contest Configuration ===
today = datetime.now()
start_of_week = today - timedelta(days=today.weekday() + 1)  # Move to Sunday
start_date = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d")
end_of_week = start_of_week + timedelta(days=6)  # Move to Saturday
end_date = end_of_week.replace(hour=23, minute=59, second=59, microsecond=0).strftime("%Y-%m-%d")

contests = [
    {
        "title": "Weekly ATS Streaks",
        "total_prize": "$100",
        "duration": "Weekly",
        "start_date": start_date,
        "end_date": end_date,
        "url": "https://sure-odds.com/",
    },
    # {
    #     "title": "Monthly ATS Streaks",
    #     "total_prize": "$250",
    #     "duration": "Monthly",
    #     "start_date": start_date,
    #     "end_date": end_date,
    #     "url": "https://sure-odds.com/",
    # }
]

intro_templates = [
    "💸 **Make picks. Go on a streak. Win real money — without betting a dime.**\n\nThe **{title}** pays the best pickers **{total_prize}** every **{duration}**. Contest starts {start_date} and ends {end_date}. Are you streak-worthy?",

    "🤑 **No bets. No fees. Just your picks.**\n\nThe **{title}** gives away **{total_prize}** each **{duration}** to users who can go on the hottest streak. Contest starts {start_date} and ends {end_date}. Start your run today.",

    "🔥 **Streak to the top and win real cash — free.**\n\nIn the **{title}**, the best streak wins. Contest starts {start_date} and ends {end_date}. Just make correct picks. Win real prizes. No risk, no cost. Just results.",

    "🎯 **The challenge is simple: pick winners every day. The reward? Real cash.**\n\nJoin the **{title}**, build your streak, and grab your share of **{total_prize}**. Contest starts {start_date} and ends {end_date}. 100% free to enter.",
]

subject_line_templates = [
    "🔥 Ready to build your betting streak?",
    "⚽ Today’s matchup + cash prize up for grabs!",
    "💸 Win cash prizes in this week’s contest!",
    "🎯 One pick. One streak. Real prizes.",
    "📈 Are you hot or not? Start your streak today.",
    "🧠 Let your betting skills pay off this week!",
    "💥 Predict winners. Win prizes. Repeat."
]

def get_subject_line():
    return random.choice(subject_line_templates)

def get_featured_matchup_spread():
    league_key = random.choice(list(leagues.keys()))
    league_name = leagues[league_key]
    emoji = sport_emojis.get(league_key, "")

    url = (
        f"https://api.the-odds-api.com/v4/sports/{league_key}/odds/"
        f"?apiKey=402f2e4bba957e5e98c7e1a178393c8c&regions=us&markets=spreads&oddsFormat=american&bookmakers=draftkings"
    )
    res = requests.get(url)
    if res.status_code != 200:
        return "⚠️ Could not fetch spread lines today."

    games = res.json()
    if not games:
        return "⚠️ No matchups available with spreads."

    game = random.choice(games)
    home = game.get("home_team")
    away = game.get("away_team")

    try:
        outcomes = game["bookmakers"][0]["markets"][0]["outcomes"]
        spreads = {o["name"]: o["point"] for o in outcomes}
        home_spread = spreads.get(home, "?")
        away_spread = spreads.get(away, "?")

        return f"""{emoji} **{home} vs {away}** – *{league_name}*

🏈 **Spread Line:**
- {home}: {home_spread:+}
- {away}: {away_spread:+}
"""
    except:
        return "⚠️ Could not parse spread data properly."

def get_league_news(league_key):
    espn_map = {
        "basketball_wnba": "wnba",
    }
    espn_key = espn_map.get(league_key)
    if not espn_key:
        return "⚠️ No ESPN news available for this league."

    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{espn_key}/news"
        if "basketball" in league_key:
            url = url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/{espn_key}/news"
        elif "icehockey" in league_key:
            url = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/news"

        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        articles = data.get("articles", [])[:3]

        headlines = "\n".join(
            f"- [{a['headline']}]({a['links']['web']['href']})"
            for a in articles if 'headline' in a
        )
        return headlines or "No major headlines today."
    except Exception as e:
        return f"⚠️ Error fetching news: {e}"


def get_our_pick_spread():
    league_key = random.choice(list(leagues.keys()))
    url = (
        f"https://api.the-odds-api.com/v4/sports/{league_key}/odds/"
        f"?apiKey=402f2e4bba957e5e98c7e1a178393c8c&regions=us&markets=spreads&oddsFormat=american&bookmakers=draftkings"
    )
    res = requests.get(url)
    if res.status_code != 200:
        return "⚠️ Could not fetch today’s ATS pick."

    games = res.json()
    if not games:
        return "⚠️ No picks available right now."

    game = random.choice(games)
    home = game.get("home_team")
    away = game.get("away_team")
    spreads = {
        o["name"]: o["point"]
        for o in game["bookmakers"][0]["markets"][0]["outcomes"]
    }

    pick_team = random.choice([home, away])
    spread = spreads.get(pick_team, "?")
    return f"📌 **Our Pick Today:** {pick_team} {spread:+} ATS"


def build_newsletter(subject_line):
    date_str = datetime.now().strftime("%A, %B %d, %Y")
    contest = random.choice(contests)
    intro = random.choice(intro_templates).format(**contest)

    # Use same league across sections
    league_key = random.choice(list(leagues.keys()))
    featured = get_featured_matchup_spread()
    news = get_league_news(league_key)
    pick = get_our_pick_spread()

    return f"""📬 **Suggested Subject Line:** _{subject_line}_

# 📅 {date_str} | Sure-Odds Streak Contest

---

{intro}

---

## 🎯 Featured Matchup with Spread

{featured}

---

## ✅ Our ATS Pick

{pick}

---

## 🗞 League Headlines

{news}

---

💥 **Think you can go on a winning run?**
[Enter here to play free →]({contest['url']})
🔥 New picks daily. {contest['total_prize']} in {contest['duration']} prizes. No cost to play.
"""

def push_to_google_doc(markdown_text):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('docs', 'v1', credentials=creds)
    doc = service.documents().create(body={"title": DOCUMENT_TITLE}).execute()
    doc_id = doc['documentId']

    service.documents().batchUpdate(documentId=doc_id, body={
        'requests': [{
            'insertText': {
                'location': {'index': 1},
                'text': markdown_text
            }
        }]
    }).execute()

    print(f"✅ Newsletter sent to Google Docs: https://docs.google.com/document/d/{doc_id}/edit")

def post_daily_newsletter():
    try:
        print("🚀 Building newsletter...")
        subject_line = get_subject_line()
        newsletter = build_newsletter(subject_line)
        push_to_google_doc(newsletter)
        print(f"📬 Suggested Subject: \"{subject_line}\"")
    except Exception as e:
        print(f"❌ Error: {e}")

# Run the task
post_daily_newsletter()
