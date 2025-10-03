# from bs4 import BeautifulSoup
# import requests
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException

browser_driver = Service('C:/Users/giorg/OneDrive/Υπολογιστής/chromedriver-win64/chromedriver.exe')

page_to_scrape = webdriver.Chrome(service=browser_driver)
page_to_scrape.get("https://www.dunkest.com/en/euroleague/stats/players/table?season_id=17&mode=nba&stats_type=avg&date_from=2024-10-03&date_to=2025-04-10&teams[]=31&teams[]=32&teams[]=33&teams[]=34&teams[]=35&teams[]=36&teams[]=37&teams[]=38&teams[]=39&teams[]=40&teams[]=41&teams[]=42&teams[]=43&teams[]=44&teams[]=45&teams[]=47&teams[]=48&teams[]=60&positions[]=1&positions[]=2&positions[]=3&player_search=&min_cr=4&max_cr=35&sort_by=pdk&sort_order=desc")

file = open("euroleague.csv", "w", newline="", encoding="utf-8-sig")
writer = csv.writer(file)

writer.writerow(["PLAYER", "POSITION", "TEAM", "F-POINTS", "COST"])

current_page = 1

try:
  page_to_scrape.find_element(By.CSS_SELECTOR, "button.iubenda-cs-close-btn").click()
  print("Closed Cookies")
  time.sleep(5)

except NoSuchElementException:
  print("No cookie concent popup found.")

while True:
  rows = page_to_scrape.find_elements(By.CSS_SELECTOR, "table tbody tr")
  for row in rows:
    player_name = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text.strip()
    position = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text.strip()
    team = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text.strip()
    f_points = row.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.strip()
    cost = row.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text.strip()
    writer.writerow([player_name, position, team, f_points, cost])
  time.sleep(1)
  next_page = str(current_page + 1)

  try:
    page_to_scrape.find_element(By.LINK_TEXT, f"{next_page}").click()
    current_page += 1
  except NoSuchElementException:
    print("didn't get a new page")
    break


file.close()