import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time


def fetch_medal_data(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(5)  # Wait for any dynamic content to load

    try:
        buttons = driver.find_elements_by_class_name(
            'message-component message-button no-children focusable buttons-row sp_choice_type_11').click
        print("Success2")
        if buttons:
            buttons[1].click()
            print("Success")
    except Exception as e:
        print("3 Error handling overlays or clicking the cookie button:", e)

    html = driver.page_source  # Fetch the page source after all interactions
    time.sleep(5)
    driver.quit()  # Now you can safely close the driver


    if html:
        return BeautifulSoup(html, 'html.parser')
    else:
        print("Failed to retrieve or parse page")
        return None


def parse_medals(soup):
    rows = soup.find_all('tbody', class_="svelte-1pwyfrz")
    medal_data = []
    for row in rows:
        country = row.find('div', {"data-key": "name"}).text.strip()
        gold = row.find('div', {"data-key": "gold"}).text.strip()
        silver = row.find('div', {"data-key": "silver"}).text.strip()
        bronze = row.find('div', {"data-key": "bronze"}).text.strip()
        medal_data.append({
            'country': country,
            'gold': gold,
            'silver': silver,
            'bronze': bronze
        })
    return medal_data


if __name__ == '__main__':
    url = 'https://www.bloomberg.com/graphics/paris-2024-summer-olympics-medal-count/'
    html_soup = fetch_medal_data(url)
    if html_soup:
        results = parse_medals(html_soup)
        print(results)
