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


def aggregate_handicappers(bets):
    handicappers = {}
    now = datetime.now()
    one_week_ago = now - timedelta(weeks=1)

    for bet in bets:
        posted_time = datetime.fromisoformat(bet['postedTime']).replace(tzinfo=None)
        if posted_time < one_week_ago:
            continue

        if bet['betResult'] is None:
                continue

        odds = int(bet['odds'])
        username = bet.get('twitterUsername', 'Anonymous')
        if username not in handicappers:
            handicappers[username] = {
                'totalOdds': 0,
                'totalWonOdds': 0,
                'numberOfBets': 0,
                'numberOfBetsWon': 0,
                'potentialWins': 0,
                'socialType': bet['socialType'],
            }
        handicappers[username]['totalOdds'] += odds
        handicappers[username]['numberOfBets'] += 1
        if bet['betResult'] == 'won':
            handicappers[username]['totalWonOdds'] += odds
            handicappers[username]['numberOfBetsWon'] += 1
            if odds > 0:
                handicappers[username]['potentialWins'] += 100 * (odds / 100)
            else:
                handicappers[username]['potentialWins'] += 100 * (100 / abs(odds))

    return sorted(
        [
            {
                'username': username,
                'totalOdds': data['totalOdds'],
                'totalWonOdds': data['totalWonOdds'],
                'numberOfBets': data['numberOfBets'],
                'numberOfBetsWon': data['numberOfBetsWon'],
                'winRatio': (data['numberOfBetsWon'] / data['numberOfBets']) * 100,
                'potentialWins': data['potentialWins'],
                'socialType': data['socialType'],
            }
            for username, data in handicappers.items()
        ],
        key=lambda x: x['potentialWins'],
        reverse=True
    )



def call_sure_odds_automated_leaderbord_marketing():
    url = "https://sheet.best/api/sheets/b9c7054b-1a70-4afb-9a14-c49967e8faf8"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        aggregated_data = aggregate_handicappers(data)
        print(aggregated_data)

        # Extract top 3 cappers/bettors
        top_3 = aggregated_data[:3]

        # Construct the message
        message = "🏆 Weekly Top Cappers/Bettors 🏆\n\n"
        for i, capper in enumerate(top_3, start=1):
            username_display = f"@{capper['username']}" if capper['socialType'] == 'twitter' else capper['username']
            message += f"{i}. {username_display} - Potential Wins: ${capper['potentialWins']:.2f}\n"

        print(message)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    # Authenticate with Twitter API
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # message = (
    #     "🚀 Boost Your Server with Top Sports Cappers from Sure Odds! 🏆\n"
    #     "Enhance your sports Discord with expert insights. Add 10+ top cappers today! 📈\n"
    #     "Exclusive Picks: Daily picks from top cappers. 📊\n"
    #     "Leaderboard: Real-time rankings. 🥇\n"
    #     "https://sure-odds.com/ #SportsBetting #BettingTips #GamblingTwitter"
    # )

    # Path to the image file
    # image_path1 = "./Screenshot 2024-08-10 015626.png"
    # image_path2 = "./Screenshot 2024-08-10 015737.png"

    # Upload the images to Twitter
    # media1 = api.media_upload(image_path1)
    # media2 = api.media_upload(image_path2)

        # Post the message on Twitter
    # client.create_tweet(text=message, media_ids=[media1.media_id, media2.media_id])
    client.create_tweet(text=message)
    print("Message posted on Twitter.")

    print("Script for posting optimized message on Twitter running")

# call_sure_odds_automated_leaderbord_marketing()

# Set the Eastern Time (EST) timezone
est = pytz.timezone('US/Eastern')

## Schedule the script to run at specific times
schedule.every().day.at("11:00").do(call_sure_odds_automated_leaderbord_marketing).timezone = est

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)