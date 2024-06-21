import requests
import tweepy
from datetime import datetime, timedelta
import pytz
import schedule
import time

# Your Twitter API credentials
api_key = "F2MU6zhUDEPPcU3pOxfJq7J2Y"
api_secret = "jEBgijrY1Aigsy3bpVJldv4WFwshcr2RWFWqLhAeK5QMrKX7zJ"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAFgGrQEAAAAAcRPWLTcm5Dsd5Q%2F2cYcBSpdHnVo%3DzBRuxFGDKRBqLBr7gPzSp5qeGs5WK3dmC4va8n84FUSZSWyspR"
access_token = "1646168850147295234-Zw5P0wkecRHbXyTqXbT7JJbm264t8F"
access_token_secret = "gRK0iRZ0akKe7JQOL41xIYRJri9PtbmsTCqkmfEuDXt1V"

# NBA functions (placeholders for actual implementation)
from nba_player_pts import (
    get_player_statistics_pts,
    get_player_pts_prop_odds,
    get_player_pts_prop_odds_two_hrs_ago,
    get_team_statistics_pts,
    merge_player_odds,
    getAi,
    get_ai_prediction
)

def nba_points_prop(league, market: str):
    leagueNameMapper = {
        "nba": "basketball_nba",
        "wnba": "basketball_wnba",
        "mlb": "baseball_mlb"
    }

    api_url = f"https://api.the-odds-api.com/v4/sports/{leagueNameMapper[league]}/odds/?apiKey=9a74934bfd1e9d98c6cc43068f53e7ae&regions=us&markets=h2h&oddsFormat=american&bookmakers=draftkings"
    response = requests.get(api_url)

    if response.status_code == 200:
        nba_games = response.json()
    else:
        print(f"Error in NBA games API request. Status code: {response.status_code}")
        return None

    merged_odds_by_game = {}

    for game in nba_games:
        game_id = game['id']
        home_team = game['home_team']
        away_team = game['away_team']
        player_odds = get_player_pts_prop_odds(game_id, league, market)
        player_odds_two_hrs_ago = get_player_pts_prop_odds_two_hrs_ago(game_id, league, market)

        if player_odds is None or player_odds_two_hrs_ago is None:
            print(f"No data available for game ID: {game_id}")
            continue

        player_odds['home_team'] = home_team
        player_odds['away_team'] = away_team

        merged_odds = merge_player_odds(player_odds, player_odds_two_hrs_ago, league, market)
        merged_odds_by_game[game_id] = merged_odds

    ai = getAi(merged_odds_by_game, market, league)
    prediction = get_ai_prediction(ai)  # Adapt get_ai_prediction to work without
    return prediction

def post_nba_points_prop():
    # Authenticate with Twitter API
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # Fetch NBA points props
    prediction = nba_points_prop('wnba', 'points')
    if prediction:
        message = (
            f"NBA Best Bets - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"{prediction}\n\n"
            "🔍📈 #NBA #PlayerProps #BettingInsights #SmartBets"
        )

        # Path to the image file (if needed)
        # image_path = "./iPad-Air-4-discord.com (1).png"
        # media = api.media_upload(image_path)
        # client.create_tweet(text=message, media_ids=[media.media_id])

        # Post the message on Twitter
        client.create_tweet(text=message)
        print("Message posted on Twitter.")
        print(message)
    else:
        print("No prediction available to post.")

# Set the Eastern Time (EST) timezone
est = pytz.timezone('US/Eastern')

# Schedule the script to run at specific times
schedule.every().day.at("11:55").do(post_nba_points_prop).timezone = est

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
