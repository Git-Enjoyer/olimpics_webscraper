from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from bs4 import BeautifulSoup


#url = 'https://olympics.com/en/paris-2024/medals'
# Element inside cross-origin iframe. Copy Selectors by right click on element or open iframe src url in new tab.
def fetch_medal_data(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(5)  # Allow time for the page to load

    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sp_message_iframe_1135992"))
    )
    driver.switch_to.frame(iframe)

    try:
        # Locate the button using WebDriver wait and expected conditions for visibility and clickable state
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))
        )
        # Execute JavaScript to click the button
        driver.execute_script("arguments[0].click();", button)
        print("Button clicked successfully using JavaScript")

    except Exception as e:
        print("Error handling overlays or clicking the cookie button:", e)

    html = driver.page_source
    time.sleep(5)
    driver.quit()  # Close the driver after operations are complete

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
