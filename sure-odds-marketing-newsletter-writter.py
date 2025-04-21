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
    # "basketball_nba": "NBA Basketball",
    "soccer_epl": "English Premier League",
    "soccer_germany_bundesliga": "German Bundesliga",
    "soccer_italy_serie_a": "Italian Serie A",
    "soccer_spain_la_liga": "Spanish La Liga",
    "soccer_usa_mls": "MLS",
    "icehockey_nhl": "NHL Hockey",
}

sport_emojis = {
    # "basketball_nba": "🏀",
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
    "🔥 **Keep your streak alive and climb the leaderboard!** 🔥\n\nCompete in the **{title}** for your shot at **{total_prize}** in FREE prizes this **{duration}**!",
    "🏆 **Ready to go on a hot streak?**\n\nJoin the **{title}** and predict winners daily. The longer your streak, the bigger your prize!",
    "💸 **Free to enter. Real cash up for grabs.**\n\nStart your streak today in the **{title}** and win up to **{total_prize}** this **{duration}**!",
]

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

def build_newsletter():
    date_str = datetime.now().strftime("%A, %B %d, %Y")
    intro = random.choice(intro_templates).format(**contest_info)

    return f"""# 📅 {date_str} | Sure-Odds Streak Contest

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

    # Insert Markdown text (plain for now)
    service.documents().batchUpdate(documentId=doc_id, body={
        'requests': [{
            'insertText': {
                'location': {'index': 1},
                'text': markdown_text
            }
        }]
    }).execute()

    print(f"✅ Newsletter sent to Google Docs: https://docs.google.com/document/d/{doc_id}/edit")

# Function to run the full task
def post_daily_newsletter():
    try:
        print("🚀 Building newsletter...")
        newsletter = build_newsletter()
        push_to_google_doc(newsletter)
    except Exception as e:
        print(f"❌ Error: {e}")

# Schedule the job
# schedule.every().day.at("06:00").do(post_daily_newsletter)

# print("🕒 Newsletter bot started. Waiting for scheduled time...")

# # Infinite loop to run the scheduler
# while True:
#     schedule.run_pending()
#     time.sleep(1)

post_daily_newsletter()
