
from numpy import log
import requests
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime, timedelta

# this is league keys for odds API
leagueNameMapper = {
    "nba": "basketball_nba",
    "wnba": "basketball_wnba",
    "mlb": "baseball_mlb"
}

#this is for our internal player data API
playerPropMapper = {
    'blocks': "blocks",
    "points": "points",
    "assists": "assists",
    'rebounds': "rebounds",
    'steals': "steals",
    "pra": "pointsReboundsAssists",
    "pa": "pointsAssists",
    "pr": "pointsRebounds",
    "ra": "reboundsAssists",
    "p_strikeouts": "pitcherStrikeouts",
    "p_walks": "pitcherWalks",
    "p_hits": "pitcherHits",
}

# This is for how the info will display in UI
propDisplayNames = {
    'blocks': "blocks",
    "points": "points",
    "assists": "assists",
    "rebounds": "rebounds",
    "steals": "steals",
    "pra": "pts + rebs + asts",
    "pa": "pts + asts",
    "pr": "pts + rebs ",
    "ra": "rebs + asts",
    "p_strikeouts": "Pitcher Strikeouts",
    "p_walks": "Pitcher Walks",
    "p_hits": "Pitcher Hits",
}

# this is for odds API markets keys
marketMappers = {
    'blocks': "player_blocks",
    "points": "player_points",
    "assists": "player_assists",
    'rebounds': "player_rebounds",
    'steals': "player_steals",
    "pra": "player_points_rebounds_assists",
    "pa": "player_points_assists",
    "pr": "player_points_rebounds",
    "ra": "player_rebounds_assists",
    "p_strikeouts": "pitcher_strikeouts",
    "p_walks": "pitcher_walks",
    "p_hits": "pitcher_hits_allowed",
}

#these are apis called for player data
playerStatsApis = {
    "nba": {
        "points":
        "https://sheet.best/api/sheets/6ffde7e5-71ac-4827-b162-18ba2d90ecb9",
        "blocks":
        "https://sheet.best/api/sheets/6ffde7e5-71ac-4827-b162-18ba2d90ecb9/tabs/NBA_Player_Props_Blocks",
        "assists":
        "https://sheet.best/api/sheets/6ffde7e5-71ac-4827-b162-18ba2d90ecb9/tabs/NBA_Player_Props_Assists",
        "rebounds":
        "https://sheet.best/api/sheets/6ffde7e5-71ac-4827-b162-18ba2d90ecb9/tabs/NBA_Player_Props_Rebounds",
        "steals":
        "https://sheet.best/api/sheets/6ffde7e5-71ac-4827-b162-18ba2d90ecb9/tabs/NBA_Player_Props_Steals",
        "pra":
        "https://sheet.best/api/sheets/d7b3e6fa-d70f-4b28-8303-1e7e31446faa",
        "pa":
        "https://sheet.best/api/sheets/d7b3e6fa-d70f-4b28-8303-1e7e31446faa/tabs/NBA_Player_Props_Points_Assists",
        "pr":
        "https://sheet.best/api/sheets/d7b3e6fa-d70f-4b28-8303-1e7e31446faa/tabs/NBA_Player_Props_Points_Rebounds",
        "ra":
        "https://sheet.best/api/sheets/d7b3e6fa-d70f-4b28-8303-1e7e31446faa/tabs/NBA_Player_Props_Rebounds_Assists"
    },
    "wnba": {
        "points":
        "https://sheet.best/api/sheets/3e2f3059-39e3-4e13-bb45-8f55fb9cd88e",
        "blocks":
        "https://sheet.best/api/sheets/3e2f3059-39e3-4e13-bb45-8f55fb9cd88e/tabs/WNBA_Player_Props_Blocks",
        "assists":
        "https://sheet.best/api/sheets/3e2f3059-39e3-4e13-bb45-8f55fb9cd88e/tabs/WNBA_Player_Props_Assists",
        "rebounds":
        "https://sheet.best/api/sheets/3e2f3059-39e3-4e13-bb45-8f55fb9cd88e/tabs/WNBA_Player_Props_Rebounds",
        "steals":
        "https://sheet.best/api/sheets/3e2f3059-39e3-4e13-bb45-8f55fb9cd88e/tabs/WNBA_Player_Props_Steals",
    },
    "mlb": {
        "p_strikeouts":
        "https://sheet.best/api/sheets/02466f37-6aab-4994-bb71-008f5c73aff3",
        "p_walks":
        "https://sheet.best/api/sheets/02466f37-6aab-4994-bb71-008f5c73aff3/tabs/MLB_Player_Props_Model_Walks",
        "p_hits":
        "https://sheet.best/api/sheets/02466f37-6aab-4994-bb71-008f5c73aff3/tabs/MLB_Player_Props_Model_Hits",
    }
}


def merge_player_odds(current_odds, odds_two_hrs_ago, league, market):
  merged_odds = {
      'home_team': current_odds['home_team'],
      'away_team': current_odds['away_team'],
      'players': {}
  }

  # Process current odds
  for bookmaker in current_odds['bookmakers']:
    for market_dict in bookmaker['markets']:
      if market_dict['key'] == marketMappers[market]:
        for outcome in market_dict['outcomes']:
          player_name = outcome['description']
          if player_name not in merged_odds['players']:
            merged_odds['players'][player_name] = {
                'current': {},
                'two_hours_ago': {}
            }
          if outcome['name'] == 'Over':
            merged_odds['players'][player_name]['current']['over'] = outcome[
                'price']
            merged_odds['players'][player_name]['current']['point'] = outcome[
                'point']
          elif outcome['name'] == 'Under':
            merged_odds['players'][player_name]['current']['under'] = outcome[
                'price']
            merged_odds['players'][player_name]['current']['point'] = outcome[
                'point']

  # Process odds from two hours ago
  for bookmaker in odds_two_hrs_ago['data']['bookmakers']:
    for market_dict in bookmaker['markets']:
      if market_dict['key'] == marketMappers[market]:
        for outcome in market_dict['outcomes']:
          player_name = outcome['description']
          if player_name not in merged_odds['players']:
            merged_odds['players'][player_name] = {
                'current': {},
                'two_hours_ago': {}
            }
          if outcome['name'] == 'Over':
            merged_odds['players'][player_name]['two_hours_ago'][
                'over'] = outcome['price']
            merged_odds['players'][player_name]['two_hours_ago'][
                'point'] = outcome['point']
          elif outcome['name'] == 'Under':
            merged_odds['players'][player_name]['two_hours_ago'][
                'under'] = outcome['price']
            merged_odds['players'][player_name]['two_hours_ago'][
                'point'] = outcome['point']

  return merged_odds


# Define functions to calculate line movement and market sentiment
def calculate_line_movement(old_odds, new_odds):
  if old_odds == 0:
    return 0  # or you can choose another appropriate default value
  return abs(((new_odds - old_odds) / old_odds) * 100)


def calculate_market_sentiment(old_odds, new_odds):
  if new_odds > old_odds:
    return "positive market sentiment"
  elif new_odds < old_odds:
    return "negative market sentiment"
  else:
    return "no significant change in market sentiment"


def getAi(merged_odds, market, league):
  ai = {}

  for game_id, game_data in merged_odds.items():
    home_team = game_data['home_team']
    away_team = game_data['away_team']
    game_prompt = f"From the following {league} game data between {home_team} and {away_team}, select the {market} best bets out of all the players for this game. Note Structure picks in bullet point format. also have a maximum of 3 best picks, each bullet point should not be greater than 10 words:\n"

    for player_name, odds_data in game_data['players'].items():
      stats = get_player_statistics_pts(player_name, league, market)
      print("stats", stats)

      if odds_data['current'].get('point') is not None:
        player_prompt = (
            f"Player: {player_name} {propDisplayNames[market]} line has been {odds_data['current']['point']} in the last two hours. "
            f"The odds to hit the over {odds_data['current']['point']} have moved from {odds_data['two_hours_ago'].get('over', 'N/A')} to {odds_data['current'].get('over', 'N/A')}, meaning there's a change of "
            f"{calculate_line_movement(odds_data['two_hours_ago'].get('over', 0), odds_data['current'].get('over', 0))}% in the last two hours, indicating "
            f"{calculate_market_sentiment(odds_data['two_hours_ago'].get('over', 0), odds_data['current'].get('over', 0))}.\n"
            f"The odds to hit the under {odds_data['current']['point']} have moved from {odds_data['two_hours_ago'].get('under', 'N/A')} to {odds_data['current'].get('under', 'N/A')}, meaning there's a change of "
            f"{calculate_line_movement(odds_data['two_hours_ago'].get('under', 0), odds_data['current'].get('under', 0))}% in the last two hours, indicating "
            f"{calculate_market_sentiment(odds_data['two_hours_ago'].get('under', 0), odds_data['current'].get('under', 0))}.\n"
        )

        if stats is not None:
          player_prompt += (
              f"Here are {player_name}'s recent {propDisplayNames[market]} performance: {propDisplayNames[market]} Last Game {stats[f'{playerPropMapper[market]}LastGame']}, {propDisplayNames[market]} 2 games ago {stats[f'{playerPropMapper[market]}TwoGamesAgo']}, "
              f"{propDisplayNames[market]} 3 games ago {stats[f'{playerPropMapper[market]}ThreeGamesAgo']}, {propDisplayNames[market]} 4 games ago {stats[f'{playerPropMapper[market]}FourGamesAgo']}, {propDisplayNames[market]} 5 games ago {stats[f'{playerPropMapper[market]}FiveGamesAgo']}.\n"
          )
        game_prompt += player_prompt
      else:
        if stats is not None:
            game_prompt += f"Here are {player_name}'s recent {propDisplayNames[market]} performance: Last Game {stats[f'{playerPropMapper[market]}LastGame']}, {propDisplayNames[market]} 2 games ago {stats[f'{playerPropMapper[market]}TwoGamesAgo']}, {propDisplayNames[market]} 3 games ago {stats[f'{playerPropMapper[market]}ThreeGamesAgo']}, {propDisplayNames[market]} 4 games ago {stats[f'{playerPropMapper[market]}FourGamesAgo']}, {propDisplayNames[market]} 5 games ago {stats[f'{playerPropMapper[market]}FiveGamesAgo']}. Will {player_name} go over or under their {propDisplayNames[market]} 5 game average in her next game. Note calculate their average and use that to determine if they go over or under. \n"
        else:
            game_prompt += f"Statistics for {player_name} are not available.\n"

    ai[game_id] = {
        'home_team': home_team,
        'away_team': away_team,
        'prompt': game_prompt
    }
    print("game_prompt", game_prompt)

  return ai


# Function to get player statistics by name
def get_player_statistics_pts(player_name, league, market):
  print("Market received:", market)  # Debugging statement
  if market not in marketMappers:
    print(f"Error: market '{market}' not found in marketMappers")
    return None

  if league not in playerStatsApis:
    print(f"Error: league '{league}' not found in playerStatsApis")
    return None

  if market not in playerStatsApis[league]:
    print(
        f"Error: market '{market}' not found in playerStatsApis for league '{league}'"
    )
    return None

  print("1", marketMappers[market])
  print("2", playerStatsApis[league][market])
  api_url = playerStatsApis[league][market]
  response = requests.get(api_url)

  if response.status_code == 200:
    player_data = response.json()
    # Find player by name
    for player in player_data:
      if player['player'].lower() == player_name.lower():
        return player
    return None
  else:
    print(
        f"Error in player statistics API request. Status code: {response.status_code}"
    )
    return None


# Function to get player prop odds for a specific game
def get_player_pts_prop_odds(game_id, league, market):
  api_url = f"https://api.the-odds-api.com/v4/sports/{leagueNameMapper[league]}/events/{game_id}/odds?apiKey=9a74934bfd1e9d98c6cc43068f53e7ae&regions=us&markets={marketMappers[market]}&oddsFormat=american&bookmakers=fanduel"
  response = requests.get(api_url)

  if response.status_code == 200:
    odds_data = response.json()
    # Find player odds for the specified player

    return odds_data
  else:
    print(
        f"Error in player prop odds API request. Status code: {response.status_code}"
    )
    return None


# Function to get player prop odds for a specific game from 2 hrs ago
def get_player_pts_prop_odds_two_hrs_ago(game_id, league, market):
  timestamp_two_hrs_ago = (datetime.utcnow() -
                           timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")

  api_url = f"https://api.the-odds-api.com/v4/historical/sports/{leagueNameMapper[league]}/events/{game_id}/odds?regions=us&apiKey=9a74934bfd1e9d98c6cc43068f53e7ae&date={timestamp_two_hrs_ago}&markets={marketMappers[market]}&oddsFormat=american&bookmakers=fanduel"

  response = requests.get(api_url)

  if response.status_code == 200:
    odds_data = response.json()

    return odds_data
  else:
    print(
        f"Error in player prop odds API request. Status code: {response.status_code}"
    )
    return None


# Function to get team statistics
def get_team_statistics_pts(team_name):
  api_url = "https://sheet.best/api/sheets/91dd5bdf-326d-4e49-bb4c-68467206df6a"
  response = requests.get(api_url)

  if response.status_code == 200:
    team_stats = response.json()
    # Find team stats by name
    for team in team_stats:
      if team['teamName'].lower() == team_name.lower():
        return team
    return None
  else:
    print(
        f"Error in team statistics API request. Status code: {response.status_code}"
    )
    return None


# Function to get AI prediction and send as message to twitter
async def get_ai_prediction(ai_data):
    ai_api_url = 'https://streamfling-be.herokuapp.com/'

    predictions = {}
    for game_id, game_data in ai_data.items():
        ai_prompt = game_data.get('prompt')
        home_team = game_data.get('home_team')
        away_team = game_data.get('away_team')
        if ai_prompt:
            ai_response = requests.post(ai_api_url,
                                        json={'prompt': ai_prompt},
                                        headers={'Content-Type': 'application/json'})
            if ai_response.status_code == 200:
                ai_data = ai_response.json()
                ai_prediction_object = ai_data.get('bot')
                ai_prediction = ai_prediction_object.get('content')
                predictions[game_id] = ai_prediction
            else:
                # Handle API error, for example by logging or setting a placeholder
                predictions[game_id] = "Error retrieving prediction"
    return predictions
