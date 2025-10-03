import pandas as pd
import numpy as np
import requests
import csv

# Get the Overall Data

url = "https://www.dunkest.com/api/stats/table"

# Define the query parameters as a dictionary
params = {
    "season_id": 17,
    "mode": "nba",
    "stats_type": "avg", # tot
    #"weeks[]": [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    #"rounds[]": [1, 2, 3],
    "date_from": "2024-10-03",
    "date_to": "2025-05-31",
    "teams[]": [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 48, 60],
    "positions[]": [1, 2, 3],
    "player_search": "",
    "min_cr": 4,
    "max_cr": 35,
    "sort_by": "pdk",
    "sort_order": "desc",
    "iframe": "yes"
}

# Define the headers for the request
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "el-GR,el;q=0.9,en;q=0.8,es;q=0.7,de;q=0.6,it;q=0.5",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

# Make the GET request
response = requests.get(url, params=params, headers=headers)



# Check the response status
if response.status_code == 200:
    print("Request was successful!")
    file = open("euroleague2.csv", "w", newline="", encoding="utf-8-sig")
    writer = csv.writer(file)
    writer.writerow(["PLAYER", "POSITION", "TEAM", "F-POINTS", "COST"])
    data = response.json()  # Parse the JSON response
    for row in data:
        player_name = row["slug"]
        position = row["position"]
        team = row["team_name"]
        fantasy_points = row["pdk"]
        cost = row["cr"]
        writer.writerow([player_name, position, team, fantasy_points, cost])
    #print(data)  # Print or handle the data as needed
    file.close()
else:
    print(f"Request failed with status code {response.status_code}")


df=pd.DataFrame(data)
print(df)