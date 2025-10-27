from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import sys

# Get date now in Greek time
now_Greek = str(datetime.now(ZoneInfo("Europe/Athens")).date())

# Get players to check the current round (gameday)
url = "https://www.dunkest.com/api/stats/table?season_id=24&mode=nba&stats_type=avg&date_from=2025-09-30&date_to=2026-05-01&teams%5B%5D=49&teams%5B%5D=50&teams%5B%5D=51&teams%5B%5D=52&teams%5B%5D=58&teams%5B%5D=59&teams%5B%5D=63&teams%5B%5D=64&teams%5B%5D=65&teams%5B%5D=66&teams%5B%5D=67&teams%5B%5D=68&teams%5B%5D=69&teams%5B%5D=70&teams%5B%5D=72&teams%5B%5D=73&teams%5B%5D=76&teams%5B%5D=77&teams%5B%5D=78&teams%5B%5D=79&positions%5B%5D=1&positions%5B%5D=2&positions%5B%5D=3&player_search=&min_cr=4&max_cr=35&sort_by=pdk&sort_order=desc&iframe=yes"

response = requests.get(url)
gamesPlayed = 0
if response.status_code == 200:
  data = response.json()
  for player in data:
    if int(player["gp"]) > gamesPlayed:
      gamesPlayed = int(player["gp"])
else:
  print(f"Players request failed with status code {response.status_code}")
  sys.exit(1)

gameDay = 1003 + gamesPlayed

# Get games from the upcoming gameday
url = f"https://fantaking-api.dunkest.com/api/v1/schedules/31/matchdays/{gameDay}"

response = requests.get(url)
if response.status_code == 200:
  data = response.json()
  upcomingDate = data["data"]["rounds"][0]["matches"][0]["started_at"]
  upcomingDateFixed =  upcomingDate.split("T")[0]
else:
  print(f"Matches request failed with status code {response.status_code}")
  sys.exit(1)

# Check if today is Gameday
if now_Greek == upcomingDateFixed:
  print("today is Gameday")
else:
  print("today is not Gameday")
  sys.exit(1)

print(f"Games Played: {gamesPlayed}")
print(f"Gameday number: {gameDay}")
print(f"Date now: {now_Greek}")
print(f"Upcoming gameday: {upcomingDateFixed}")