import requests
import random
import schedule
import time
from datetime import datetime
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Configs
SCOPES = ['https://www.googleapis.com/auth/documents']
DOCUMENT_TITLE = "Sure-Odds Daily Newsletter"

# Leagues & Emojis
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

contest_info = {
    "title": "Sure-Odds Streak Contest",
    "total_prize": "$500",
    "duration": "Weekly",
    "url": "https://sure-odds.com/",
}

intro_templates = [
    "💸 **Make picks. Go on a streak. Win real money — without betting a dime.**\n\nThe **{title}** pays the best pickers **{total_prize}** every **{duration}**. It’s not gambling. It’s skill. Are you streak-worthy?",

    "🤑 **No bets. No fees. Just your picks.**\n\nThe **{title}** gives away **{total_prize}** each **{duration}** to users who can go on the hottest streak. All free, all real. Start your run today.",

    "🔥 **Streak to the top and win real cash — free.**\n\nIn the **{title}**, the best streak wins. Just make correct picks. Win real prizes. No risk, no cost. Just results.",

    "🎯 **The challenge is simple: pick winners every day. The reward? Real cash.**\n\nJoin the **{title}**, build your streak, and grab your share of **{total_prize}**. 100% free to enter.",
]


subject_line_templates = [
    "🔥 Ready to build your betting streak?",
    "⚽ Today’s matchup + $500 up for grabs!",
    "💸 Win up to $500 in this week’s contest!",
    "🎯 One pick. One streak. Real prizes.",
    "📈 Are you hot or not? Start your streak today.",
    "🧠 Let your betting skills pay off this week!",
    "💥 Predict winners. Win prizes. Repeat."
]

def get_subject_line():
    return random.choice(subject_line_templates)

def get_featured_matchup():
    league_key = random.choice(list(leagues.keys()))
    league_name = leagues[league_key]
    emoji = sport_emojis[league_key]
    url = f"https://api.the-odds-api.com/v4/sports/{league_key}/odds/?apiKey=402f2e4bba957e5e98c7e1a178393c8c&regions=us&markets=h2h&oddsFormat=american&bookmakers=fanduel"

    response = requests.get(url)
    if response.status_code != 200:
        return "⚠️ Could not fetch matchups today."

    data = response.json()
    if not data:
        return "⚠️ No matchups available right now."

    game = data[0]
    home = game['home_team']
    away = game['away_team']
    prices = {o['name']: o['price'] for o in game['bookmakers'][0]['markets'][0]['outcomes']}

    odds_line = f"**{home}** ({prices.get(home)}) vs **{away}** ({prices.get(away)})"
    if "Draw" in prices:
        odds_line += f" | **Draw** ({prices['Draw']})"

    return f"{emoji} **{home} vs {away}** – *{league_name}*\n\n💰 Odds: {odds_line}"

def get_our_pick():
    league_key = random.choice(list(leagues.keys()))
    url = f"https://api.the-odds-api.com/v4/sports/{league_key}/odds/?apiKey=402f2e4bba957e5e98c7e1a178393c8c&regions=us&markets=h2h&oddsFormat=american&bookmakers=fanduel"
    response = requests.get(url)

    if response.status_code != 200:
        return "⚠️ Could not fetch our pick today."

    data = response.json()
    if not data:
        return "⚠️ No picks available right now."

    game = data[0]
    home = game['home_team']
    away = game['away_team']
    outcomes = game['bookmakers'][0]['markets'][0]['outcomes']
    pick = random.choice([home, away] + (["Draw"] if any(o["name"] == "Draw" for o in outcomes) else []))

    return f"📌 **Our Pick Today:** {pick} – based on current odds & form."


def build_newsletter(subject_line):
    date_str = datetime.now().strftime("%A, %B %d, %Y")
    intro = random.choice(intro_templates).format(**contest_info)
    featured = get_featured_matchup()
    our_pick = get_our_pick()

    return f"""📬 **Suggested Email Subject:** _{subject_line}_

# 📅 {date_str} | Sure-Odds Streak Contest

---

{intro}

---

## 🎯 Today's Featured Matchup

{featured}

---

## ✅ Our Pick

{our_pick}

---

💥 **Think you can go on a winning run?**

[Enter now]({contest_info['url']})

🔥 New matchups posted daily. The streak starts with one pick.
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
