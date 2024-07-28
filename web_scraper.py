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

def fetch_medal_data(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    try:
        # Locate the button using WebDriver wait and expected conditions for visibility and clickable state
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Yes, I agree']"))
        )
        # Execute JavaScript to click the button
        driver.execute_script("arguments[0].click();", button)
        print("Button clicked successfully using JavaScript")

    except Exception as e:
        print("Error handling overlays or clicking the cookie button:", e)

    html = driver.page_source
    driver.quit()  # Close the driver after operations are complete

    if html:
        return BeautifulSoup(html, 'html.parser')
    else:
        print("Failed to retrieve or parse page")
        return None

def parse_medals(soup):
    #print(soup)
    rows = soup.find_all('tr', class_='ssrcss-dhlz6k-TableRowBody e1xoxfm60')
    medal_data = []
    for row in rows:
        country = row.find('span', class_='ssrcss-pek3um-AbbreviatedCountryName ew4ldjd1').text.strip()
        gold = row.find('td', class_='ssrcss-fvkmzs-StyledTableData ef9ipf1').text.strip()
        silver = row.find('td', class_='ssrcss-fvkmzs-StyledTableData ef9ipf1').text.strip()
        bronze = row.find('td', class_='ssrcss-fvkmzs-StyledTableData ef9ipf1').text.strip()

        medal_data.append({
            'country': country,
            'gold': gold,
            'silver': silver,
            'bronze': bronze
        })
    return medal_data


if __name__ == '__main__':
    url = 'https://www.bbc.co.uk/sport/olympics/paris-2024/medals'
    html_soup = fetch_medal_data(url)
    if html_soup:
        results = parse_medals(html_soup)
        print(results)
