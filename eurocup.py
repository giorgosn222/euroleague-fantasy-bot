import requests
import csv

# Arrays to fill
players = []
matches = []
teams = []

# GET PLAYER DATA
url1 = "https://www.dunkest.com/api/stats/table?season_id=24&mode=nba&stats_type=avg&date_from=2025-09-30&date_to=2026-05-01&teams%5B%5D=49&teams%5B%5D=50&teams%5B%5D=51&teams%5B%5D=52&teams%5B%5D=58&teams%5B%5D=59&teams%5B%5D=63&teams%5B%5D=64&teams%5B%5D=65&teams%5B%5D=66&teams%5B%5D=67&teams%5B%5D=68&teams%5B%5D=69&teams%5B%5D=70&teams%5B%5D=72&teams%5B%5D=73&teams%5B%5D=76&teams%5B%5D=77&teams%5B%5D=78&teams%5B%5D=79&positions%5B%5D=1&positions%5B%5D=2&positions%5B%5D=3&player_search=&min_cr=4&max_cr=35&sort_by=pdk&sort_order=desc&iframe=yes"

response = requests.get(url1)

if response.status_code == 200:
	print("Players request was successful!")
	data = response.json()
	for player in data:
		if float(player["cr"]) == 0:
			continue
		else:
			players.append(
				{
					"id": player["id"],
					"games": player["gp"],
					"name": player["last_name"] + " " + player["first_name"],
					"team_code": player["team_code"],
					"team_name": player["team_name"],
					"position": player["position"],
					"position_id": player["position_id"],
					"credits": float(player["cr"]),
					"points": float(player["pdk"])
				}
			)
else:
	print(f"Players request failed with status code {response.status_code}")

gamesPlayed = 0
for player in players:
	if int(player["games"]) > gamesPlayed:
		gamesPlayed = int(player["games"])

# GET MATCHES
gameDay = 1003 + gamesPlayed

url2 = f"https://fantaking-api.dunkest.com/api/v1/schedules/31/matchdays/{gameDay}"

response = requests.get(url2)
if response.status_code == 200:
	print("Matches request was successful!")
	data = response.json()
	for round in data["data"]["rounds"]:
		for match in round["matches"]:
			matches.append({
				"home_team": match["home_team"]["name"],
				"away_team": match["away_team"]["name"]
			})
else:
	print(f"Matches request failed with status code {response.status_code}")

# ADD OPP TO EACH PLAYER
for player in players:
	for match in matches:
		if match["home_team"] == player["team_name"]:
			player["opp"] = match["away_team"]
		elif match["away_team"] == player["team_name"]:
			player["opp"] = match["home_team"]

# GET TEAMS' ALLOWED F-POINTS
for i in range(1, 4):
	url3 = f"https://www.dunkest.com/api/stats/defense-vs-position?season_id=24&stats_id=25&position_id={i}"

	response = requests.get(url3)
	if response.status_code == 200:
		print(f"Teams {i} request was successful!")
		data = response.json()
		for team in data:
			teamExist = False
			for existingTeam in teams:
				if existingTeam["name"] == team["name"]:
					existingTeam[str(i)] = team["all"]
					teamExist = True
			if teamExist == False:
				teams.append({
					"name": team["name"],
					str(i): team["all"]
				})
	else:
		print(f"Teams request failed with status code {response.status_code}")

# ADD ALLOWED POINTS TO EACH PLAYER
for player in players:
	opp = player.get("opp")
	position = player["position_id"]

	if opp:
		for team in teams:
			if team["name"] == opp:
				player["allowed_points"] = float(team[position])

# MAKE CSV FILE
file = open("Eurocup Fantasy 2025-2026.csv", "w", newline="", encoding="utf-8-sig")
writer = csv.writer(file)

writer.writerow(["NAME", "TEAM", "POSITION", "CREDITS", "POINTS", "POINTS PER CREDIT", "AVERAGE + ALLOWED POINTS"])

for player in players:
	writer.writerow([
		player["name"],
		player["team_code"],
		player["position"],
		player["credits"],
		player["points"],
		player["points"] / player["credits"],
		player["points"] + player.get("allowed_points", 0.0),
	])

file.close()
