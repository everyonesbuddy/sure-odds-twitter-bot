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
    "soccer_epl": "English Premier League",
    "soccer_germany_bundesliga": "German Bundesliga",
    "soccer_italy_serie_a": "Italian Serie A",
    "soccer_spain_la_liga": "Spanish La Liga",
    "soccer_usa_mls": "MLS",
    "icehockey_nhl": "NHL Hockey",
}

sport_emojis = {
    "soccer_epl": "⚽",
    "soccer_germany_bundesliga": "⚽",
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
    "🎯 **Everyone says they’re the best at betting. Let’s find out who actually is.**\n\nEnter the **{title}** and go on a streak to win your share of **{total_prize}** — free to play, real prizes, every **{duration}**.",
    "😤 **Tired of fake betting experts?**\n\nHere’s your chance to prove you're the real deal.\n\nJoin the **{title}** — hit a streak, climb the leaderboard, and win up to **{total_prize}** this **{duration}**.",
    "🧠 **Think you're sharp? Prove it.**\n\nThe **{title}** pays the best streaks — no entry fee, no gimmicks. Just your picks. Just skill.\n\nPlay now to win **{total_prize}** in prizes **{duration}**.",
    "💰 **The game is simple:**\nMake correct picks. Build your streak. Win real money.\n\nJoin the **{title}** and compete for **{total_prize}** this **{duration}**.\n\nFREE to enter — only skill matters.",
    "📊 **Prove you're not just talk.**\n\nJoin the **{title}** and let your picks speak.\n\nGo on a heater, win up to **{total_prize}** — no cost to enter. Your streak is your resume."
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

def build_newsletter(subject_line):
    date_str = datetime.now().strftime("%A, %B %d, %Y")
    intro = random.choice(intro_templates).format(**contest_info)

    return f"""📬 **Suggested Email Subject:** _{subject_line}_

# 📅 {date_str} | Sure-Odds Streak Contest

---

{intro}

---

## 🎯 Today's Featured Matchup

{get_featured_matchup()}

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
