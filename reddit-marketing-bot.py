import random
import requests
from datetime import datetime, timedelta

# === Constants & Config ===
API_KEY = "402f2e4bba957e5e98c7e1a178393c8c"
LEAGUES = {
    "basketball_wnba": "WNBA Basketball",
    "baseball_mlb": "MLB Baseball"
}
EMOJIS = {
    "basketball_wnba": "🏀",
    "baseball_mlb": "⚾"
}
SURE_ODDS_URL = "https://sure-odds.com"

# === Contest Configuration ===
today = datetime.now()
start_of_week = today - timedelta(days=today.weekday() + 1)  # Move to Sunday
start_date = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d")
end_of_week = start_of_week + timedelta(days=6)  # Move to Saturday
end_date = end_of_week.replace(hour=23, minute=59, second=59, microsecond=0).strftime("%Y-%m-%d")

contests = [
    {
        "title": "Weekly ATS Streaks",
        "prize": "$100",
        "duration": "weekly",
        "start_date": start_date,
        "end_date": end_date,
        "expected_streak": 5
    },
    # {
    #     "title": "Monthly ATS Streaks",
    #     "prize": "$250",
    #     "duration": "monthly",
    #     "start_date": start_date,
    #     "end_date": end_date,
    #     "expected_streak": 15
    # }
]

# === Templates ===
daily_pick_templates = [
    "🔥 My ATS Pick of the Day + Free Contest\n\nI’m riding with **{team_pick} {spread}** tonight — {reason}\n\nAlso tracking this on [Sure-Odds.com]({url}), where they’re running a **free ATS streak challenge**. Hit {expected_streak} in a row, win a **{prize}**. Weekly reset.\n\nAnyone else playing this tonight?",
    "Going for 4 in a row ATS — my pick today: **{team_pick} {spread}**\n\nI’m in this free streak contest at [Sure-Odds.com]({url}). If I hit {expected_streak} straight, I win {prize}. No betting, just pick and track.\n\nAnyone else grinding the board daily? Let’s go streak hunting 🧹"
]

giveaway_templates = [
    """🎁 Free Sports Contest – Win {prize} Every Week (No Entry Fee)

Contest starts {start_date} and ends {end_date}. Only {days_left} days left!

If you're into sports betting or daily picks, check this out:

**Sure-Odds.com** is running a free streak challenge — make daily picks, and if you hit {expected_streak} in a row, you win a **{prize}**.

No signup hoops. No betting. Just you vs the board.

🔗 [Try it free here](https://sure-odds.com)""",

    """💸 Think You Can Go {expected_streak}-0 ATS? Win {prize} Free

Contest starts {start_date} and ends {end_date}. Hurry, only {days_left} days left!

Not a sweepstake, not a sportsbook — this is a **free sports streak challenge**.

Each day, you make one pick. If you hit {expected_streak} straight, you win {prize}.

Play at [Sure-Odds.com](https://sure-odds.com)

No money needed. Just your sports brain."""
]

comment_templates = [
    "What’s going on in the league?\n{news}"
]

founder_templates = [
    """I’ve built and launched a side project for sports fans: [Sure-Odds.com](https://sure-odds.com)

It’s a free streak contest where users pick one game per day ATS. No betting, no entry fees — just pure streak-building. Weekly and monthly prizes via gift cards.

The idea came after years of losing on sportsbooks — I realized it wasn’t gambling I loved, it was the **skill challenge**.

Would love any feedback or thoughts. 🙏""",

    """After losing one too many parlays, I built a free tool for sports fans: [Sure-Odds.com](https://sure-odds.com)

It lets users make daily ATS picks and try to build streaks. Hit {expected_streak} in a row? You win {prize}. No gambling involved — just sports IQ.

Trying to blend fantasy, betting, and competition — without the risk.

Would love to hear thoughts if you check it out. Feedback = ❤️"""
]

# === Suggested Subreddits by Post Type ===
SUBREDDIT_SUGGESTIONS = {
    "Daily/Weekly Pick": ["r/sportsbook", "r/NBA_Discussion", "r/MLBTheShow", "r/nbabetting", "r/CFB"],
    "Giveaway/Contest": ["r/giveaways", "r/contest", "r/freestuff", "r/sportsbetting", "r/beermoney"],
    "Comment Drop": ["r/NBA", "r/baseball", "r/sports", "r/nfl", "r/soccer"],
    "Side Project / Founder Post": ["r/sideproject", "r/startups", "r/Entrepreneur", "r/webapps", "r/coolgithubprojects"]
}

# === Fetch Odds ===
def fetch_random_game():
    league_key = random.choice(list(LEAGUES.keys()))
    emoji = EMOJIS.get(league_key, "")
    url = (
        f"https://api.the-odds-api.com/v4/sports/{league_key}/odds/"
        f"?apiKey={API_KEY}&regions=us&markets=spreads&oddsFormat=american&bookmakers=draftkings"
    )
    try:
        res = requests.get(url)
        res.raise_for_status()
        games = res.json()
        if not games:
            print("[WARN] No games found from odds API.")
            return None

        random.shuffle(games)
        for game in games:
            bookmakers = game.get("bookmakers", [])
            if not bookmakers:
                continue
            markets = bookmakers[0].get("markets", [])
            if not markets:
                continue
            outcomes = markets[0].get("outcomes", [])
            if not outcomes:
                continue

            home = game.get("home_team", "Unknown Home")
            away = game.get("away_team", "Unknown Away")

            # Map team names to spread points
            spreads = {o["name"]: o["point"] for o in outcomes if "name" in o and "point" in o}

            # Choose randomly between home and away teams to pick
            pick_team = random.choice([home, away])

            # Get the spread for picked team, fallback to "?" if missing
            spread_value = spreads.get(pick_team, "?")

            # Format spread string with sign only if spread_value is a number
            if isinstance(spread_value, (int, float)):
                spread_str = f"{'-' if spread_value < 0 else '+'}{abs(spread_value)}"
            else:
                spread_str = "?"

            return {
                "team_pick": pick_team,
                "spread": spread_str,
                "home": home,
                "away": away,
                "league": LEAGUES.get(league_key, league_key),
                "league_key": league_key,  # for ESPN news integration
                "emoji": emoji
            }

        print("[WARN] No valid game with bookmakers and spreads found.")
        return None

    except Exception as e:
        print(f"[ERROR] Odds fetch failed: {e}")
        return None

# === Fetch ESPN Headlines ===
def fetch_espn_headlines(league_key):
    # Map the odds API league keys to ESPN league keys
    espn_league_map = {
        "basketball_wnba": "wnba",
        "baseball_mlb": "mlb"
    }
    sport_map = {
        "basketball_wnba": "basketball",
        "baseball_mlb": "baseball"
    }

    espn_league = espn_league_map.get(league_key)
    if not espn_league:
        return None

    sport = sport_map.get(league_key, "basketball")  # Default to basketball if not found

    url = f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{espn_league}/news?limit=3"

    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        articles = data.get("articles", [])

        headlines = []
        for article in articles:
            headline = article.get("headline")
            link = article.get("links", {}).get("web", {}).get("href")
            if headline and link:
                headlines.append(f"- [{headline}]({link})")
        return "\n".join(headlines) if headlines else None
    except Exception as e:
        print(f"[ERROR] ESPN news fetch failed: {e}")
        return None
# === Generator Function ===
def generate_reddit_post():
    all_templates = {
        "Daily/Weekly Pick": daily_pick_templates,
        "Giveaway/Contest": giveaway_templates,
        "Comment Drop": comment_templates,
        "Side Project / Founder Post": founder_templates
    }

    post_type = random.choice(list(all_templates.keys()))
    post_template = random.choice(all_templates[post_type])
    contest = random.choice(contests)

    # Calculate days left until contest ends
    end_date_obj = datetime.strptime(contest["end_date"], "%Y-%m-%d")
    days_left = (end_date_obj - datetime.now()).days

    if post_type == "Daily/Weekly Pick":
        game_data = fetch_random_game()
        if game_data:
            post_content = post_template.format(
                team_pick=game_data["team_pick"],
                spread=game_data["spread"],
                reason="they’ve been solid ATS recently",
                url=SURE_ODDS_URL,
                start_date=contest["start_date"],
                end_date=contest["end_date"],
                days_left=days_left,
                expected_streak=contest["expected_streak"],
                prize=contest["prize"]
            )
        else:
            post_content = "[ERROR] Could not fetch game data for daily pick."

    elif post_type == "Giveaway/Contest":
        post_content = post_template.format(
            start_date=contest["start_date"],
            end_date=contest["end_date"],
            days_left=days_left,
            expected_streak=contest["expected_streak"],
            prize=contest["prize"]
        )

    elif post_type == "Comment Drop":
        game_data = fetch_random_game()
        if game_data:
            espn_news = fetch_espn_headlines(game_data["league_key"])
            post_content = post_template.format(
                news=espn_news or "No recent headlines at the moment."
            )
        else:
            post_content = post_template.format(
                news="(Couldn't load current league headlines.)"
            )

    elif post_type == "Side Project / Founder Post":
        post_content = post_template.format(
            expected_streak=contest["expected_streak"],
            prize=contest["prize"]
        )

    print(f"\n🧵 Reddit Post Type: {post_type}\n")
    print(post_content)

    suggested_subs = SUBREDDIT_SUGGESTIONS.get(post_type, [])
    if suggested_subs:
        print("\n📌 Suggested Subreddits for Posting:")
        for sub in suggested_subs:
            print(f"- {sub}")

# === Run It ===
generate_reddit_post()
