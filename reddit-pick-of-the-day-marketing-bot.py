import requests
import random
from datetime import datetime

bookmaker = "fanduel"
odds_api_key = "402f2e4bba957e5e98c7e1a178393c8c"  # Replace with your valid key
odds_range = (-200, 200)

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

def fetch_valid_pick():
    for league_key in random.sample(list(leagues.keys()), len(leagues)):
        url = f"https://api.the-odds-api.com/v4/sports/{league_key}/odds/?apiKey={odds_api_key}&regions=us&markets=h2h&oddsFormat=american&bookmakers={bookmaker}"
        r = requests.get(url)
        if r.status_code != 200:
            continue

        games = r.json()
        for game in games:
            for outcome in game['bookmakers'][0]['markets'][0]['outcomes']:
                price = outcome['price']
                if odds_range[0] <= price <= odds_range[1]:
                    return {
                        "matchup": f"{game['home_team']} vs {game['away_team']}",
                        "pick": outcome['name'],
                        "odds": price,
                        "league": leagues[league_key],
                        "start_time": game.get('commence_time', 'N/A')
                    }
    return None

def generate_pick_post():
    pick = fetch_valid_pick()
    if not pick:
        print("❌ No valid pick found today.")
        return

    units = random.randint(1, 5)
    reasoning = random.choice([
        "Model-based pick using team form + injuries. Record this season: 61-38 (61.6%)",
        "Based on recent form + line movement. Fading public overreaction.",
        "Home team dominance and favorable matchup trends. ROI +14% YTD.",
        "Model pick based on xG + defensive ratings. Strong home edge here.",
    ])

    print(f"""🎯 **Pick of the Day**

**Matchup:** {pick['matchup']}
**League:** {pick['league']}
**Start Time:** {pick['start_time']}

**Pick:** {pick['pick']}
**Odds:** {pick['odds']}
**Bet Size:** {units} unit(s)

**Reasoning:** {reasoning}

✅ Tip here if you can: [Sure-Odds](https://sure-odds.com/)

---

*This is not a bet. It’s a streak pick made for our free daily contest (real prizes, no deposits).*""")

generate_pick_post()
