import requests
from bs4 import BeautifulSoup

#Possible URLs for medals
    #url = 'https://olympics.com/en/paris-2024/medals'
    #url = 'https://www.bloomberg.com/graphics/paris-2024-summer-olympics-medal-count/'
def fetch_medal_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print("Failed to retrieve data")
        return None


def parse_medals(soup):
    rows = soup.find_all('tbody', attrs={'class="svelte-1pwyfrz'})
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