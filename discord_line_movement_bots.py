import os
from dotenv import load_dotenv
import discord
import requests
from datetime import datetime, timedelta

intents = discord.Intents().all()
intents.members = True

client = discord.Client(intents=intents)

# Load environment variables from .env file
load_dotenv()

# Functions
#calculate Line movement function
def calculate_line_movement():
  results = []
  # Step 1: Get Event IDs
  #api_url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey=5e7c521ab26381b068424419c586233a&regions=us&markets=h2h&oddsFormat=american&bookmakers=draftkings"
  api_url = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey=5e7c521ab26381b068424419c586233a&regions=us&markets=h2h&oddsFormat=american&bookmakers=draftkings"
  response = requests.get(api_url)

  # Check if the request was successful (status code 200)
  if response.status_code != 200:
      print(f"Error in API request. Status code: {response.status_code}")
      return results

  odds_data = response.json()
  # Extract the first 5 event IDs
  event_ids = [game['id'] for game in odds_data[:5]]

  # Step 2: Iterate Through Event IDs
  for event_id in event_ids:
      # Step 3: Get Current and Previous Odds
      #current_api_url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey=5e7c521ab26381b068424419c586233a&regions=us&markets=h2h&oddsFormat=american&bookmakers=draftkings&eventIds={event_id}"
      current_api_url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey=5e7c521ab26381b068424419c586233a&regions=us&markets=h2h&oddsFormat=american&bookmakers=draftkings&eventIds={event_id}"
      current_response = requests.get(current_api_url)

      # Check if the request was successful (status code 200)
      if current_response.status_code != 200:
          print(f"Error in API request. Status code: {current_response.status_code}")
          continue

      current_odds = current_response.json()

      # Call the API to get previous odds
      previous_timestamp = (datetime.utcnow() - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
      #previous_api_url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds-history/?apiKey=5e7c521ab26381b068424419c586233a&regions=us&markets=h2h&date=2023-12-30T17:14:40Z&oddsFormat=american&eventIds={event_id}&bookmakers=draftkings"
      previous_api_url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds-history/?apiKey=5e7c521ab26381b068424419c586233a&regions=us&markets=h2h&date={previous_timestamp}&bookmakers=draftkings&oddsFormat=american&eventIds={event_id}"
      previous_response = requests.get(previous_api_url)

      # Check if the request was successful (status code 200)
      if previous_response.status_code != 200:
          print(f"Error in API request. Status code: {previous_response.status_code}")
          continue

      previous_odds = previous_response.json()

      # Step 4: Calculate Time Difference
      current_timestamp = current_odds[0]['bookmakers'][0]['markets'][0]['last_update']
      previous_timestamp = previous_odds['data'][0]['bookmakers'][0]['markets'][0]['last_update']
      current_time = datetime.strptime(current_timestamp, "%Y-%m-%dT%H:%M:%SZ")
      previous_time = datetime.strptime(previous_timestamp, "%Y-%m-%dT%H:%M:%SZ")
      time_difference = (current_time - previous_time).seconds // 3600

      # Step 5: Calculate Line Movement
      current_team_1_price = current_odds[0]['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
      previous_team_1_price = previous_odds['data'][0]['bookmakers'][0]['markets'][0]['outcomes'][0]['price']

      current_team_2_price = current_odds[0]['bookmakers'][0]['markets'][0]['outcomes'][1]['price']
      previous_team_2_price = previous_odds['data'][0]['bookmakers'][0]['markets'][0]['outcomes'][1]['price']

      line_movement_percentage_home = round(((current_team_1_price - previous_team_1_price) / abs(previous_team_1_price)) * 100,1)
      line_movement_percentage_away = round(((current_team_2_price - previous_team_2_price) / abs(previous_team_2_price)) * 100,1)

      # Step 6: Print Results
      team_1_team = current_odds[0]['bookmakers'][0]['markets'][0]['outcomes'][0]['name']
      team_2_team = current_odds[0]['bookmakers'][0]['markets'][0]['outcomes'][1]['name']

      results.append(f"{team_1_team} moneyline has moved {line_movement_percentage_home}% "
        f"from {previous_team_1_price} to {current_team_1_price} in the past {time_difference} hours.")

      results.append(f"{team_2_team} moneyline has moved {line_movement_percentage_away}% "
        f"from {previous_team_2_price} to {current_team_2_price} in the past {time_difference} hours.")

  return results

      #print(f"Home Team - {home_team} moneyline has moved {line_movement_percentage_home}% "
            #f"from {previous_home_price} to {current_home_price} in the past {time_difference} hours.")

      #print(f"Away Team - {away_team} moneyline has moved {line_movement_percentage_away}% "
            #f"from {previous_away_price} to {current_away_price} in the past {time_difference} hours.")




#onready and on message functions for discord
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  ## Start of creating our discord bot Commands##
  #command for line movement results
  if message.content.startswith("$results"):
    results = calculate_line_movement()

    # Send each prediction as a separate message
    for result in results:
      await message.channel.send(result)


client.run(os.getenv("LINE_MOVEMENT_DISCORD_TOKEN"))
