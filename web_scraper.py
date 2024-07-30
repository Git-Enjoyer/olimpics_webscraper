from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import psycopg2
from audit_logs import log_entry

# url = 'https://olympics.com/en/paris-2024/medals'

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
    rows = soup.find_all('tr', class_='ssrcss-dhlz6k-TableRowBody e1xoxfm60')
    medal_data = []
    for row in rows:
        cells = row.find_all('td', class_='ssrcss-fvkmzs-StyledTableData ef9ipf1')

        current_ranking = cells[0].find('div').text.strip() if cells[0].find('div') else 'N/A'
        country_name_div = cells[1].find('span', class_='ssrcss-ymac56-CountryName ew4ldjd0')
        country_name = country_name_div.text.strip() if country_name_div else 'N/A'

        gold = cells[2].find('div').text.strip()
        silver = cells[3].find('div').text.strip()
        bronze = cells[4].find('div').text.strip()
        overall = cells[5].find('div').text.strip()

        medal_data.append({
            'ranking': current_ranking,
            'country': country_name,
            'gold': gold,
            'silver': silver,
            'bronze': bronze,
            'overall': overall
        })
    return medal_data


def insert_data(medal_data):
    try:
        conn = psycopg2.connect(
            dbname="olympic_sweepstake",
            user="postgres",
            password="Alank@4321",
            host="localhost",
            port=5432
        )
        cursor = conn.cursor()

        # Ensure medal_data is indeed a list of dictionaries
        if not all(isinstance(item, dict) for item in medal_data):
            raise ValueError("medal_data must be a list of dictionaries")

        for data in medal_data:
            # Ensure that each dictionary has all the required keys
            if not all(key in data for key in ['ranking', 'country', 'gold', 'silver', 'bronze', 'overall']):
                raise ValueError("Each data item must contain all keys: ranking, country, gold, silver, bronze, overall")

            cursor.execute("""
                INSERT INTO countries (ranking, name, gold, silver, bronze, overall) 
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (name) DO UPDATE SET
                ranking = EXCLUDED.ranking,
                gold = EXCLUDED.gold,
                silver = EXCLUDED.silver,
                bronze = EXCLUDED.bronze,
                overall = EXCLUDED.overall
                """,
                (data['ranking'], data['country'], data['gold'], data['silver'], data['bronze'], data['overall'])
            )

        conn.commit()
        now = datetime.now()
        print(f"Data successfully updated at {now.strftime('%Y-%m-%d %H:%M:%S')}")

        log_entry(conn, 'Countries table update', True, 'Data successfully updated.')

    except psycopg2.Error as e:
        conn.rollback()
        log_entry(conn, 'Countries table update', False, f"Database error: {str(e)}")
    except Exception as e:
        conn.rollback()
        log_entry(conn, 'Countries table update', False, f"An error occurred: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    url = 'https://www.bbc.co.uk/sport/olympics/paris-2024/medals'
    html_soup = fetch_medal_data(url)
    if html_soup:
        results = parse_medals(html_soup)
        formatted_results = "\n".join(str(result) for result in results)
        print(results)
        #print(formatted_results)
        insert_data(results)

