# from bs4 import BeautifulSoup
# import requests
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException

browser_driver = Service(r'C:\Users\giorg\OneDrive\Υπολογιστής\chromedriver-win64\chromedriver.exe')

page_to_scrape = webdriver.Chrome(service=browser_driver)
page_to_scrape.get("https://quotes.toscrape.com")

page_to_scrape.find_element(By.LINK_TEXT, "Login").click()

time.sleep(3)
username = page_to_scrape.find_element(By.ID, "username")
password = page_to_scrape.find_element(By.ID, "password")
username.send_keys("admin")
password.send_keys("1234")
page_to_scrape.find_element(By.CSS_SELECTOR, "input.btn-primary").click()

file = open("scrapped_quotes.csv", "w", newline="", encoding="utf-8-sig")
writer = csv.writer(file)

writer.writerow(["QUOTES", "AUTHORS"])

while True:
  quotes = page_to_scrape.find_elements(By.CLASS_NAME, "text")
  authors = page_to_scrape.find_elements(By.CLASS_NAME, "author")

  for quote, author in zip(quotes, authors):
    print(quote.text + " - " + author.text)
    writer.writerow([quote.text, author.text])
  try:
    page_to_scrape.find_element(By.PARTIAL_LINK_TEXT, "Next").click()
  except NoSuchElementException:
    break
file.close()