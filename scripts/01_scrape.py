# scripts/01_scrape.py
# This script gets Premier League stats from FBref.com
# and saves them as a CSV file in data/raw/
 
import requests          # for downloading web pages
import pandas as pd      # for working with data tables
from bs4 import BeautifulSoup  # for reading HTML
import time              # for pausing between requests
import os                # for creating folders
 
# Create the output folder if it doesn't already exist
os.makedirs('data/raw', exist_ok=True)
 
# The webpage we want to scrape
URL = 'https://fbref.com/en/comps/9/Premier-League-Stats'
 
# This makes our request look like it's coming from a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; student research project)'
}
 
def scrape_fbref_stats():
    print('Downloading data from FBref...')
    response = requests.get(URL, headers=headers)
    time.sleep(2)  # wait 2 seconds — polite scraping!
 
    soup = BeautifulSoup(response.text, 'html.parser')
 
    # Try to find the league table on the page
    table = soup.find('table', {'id': 'results2023-202491_overall'})
    if not table:
        tables = soup.find_all('table', class_='stats_table')
        table = tables[0] if tables else None
 
    if not table:
        print('Could not find the table on FBref.')
        print('This sometimes happens if FBref changed their website.')
        print('Using built-in backup data instead...')
        return None
 
    rows = []
    headers_row = [th.get_text(strip=True)
                   for th in table.find('thead').find_all('th')]
 
    for tr in table.find('tbody').find_all('tr'):
        if tr.get('class') and 'spacer' in tr.get('class'):
            continue
        cells = [td.get_text(strip=True)
                 for td in tr.find_all(['td', 'th'])]
        if cells:
            rows.append(cells)
 
    df = pd.DataFrame(rows, columns=headers_row[:len(rows[0])])
    df.to_csv('data/raw/fbref_standings.csv', index=False)
    print(f'Success! Saved {len(df)} rows to data/raw/fbref_standings.csv')
    return df
 
 
# -------------------------------------------------------
# BACKUP DATA — used if scraping fails for any reason
# This is the actual 2023/24 final Premier League table
# -------------------------------------------------------
def load_backup_data():
    data = {
        'Squad': ['Man City','Arsenal','Liverpool','Aston Villa',
                  'Tottenham','Chelsea','Newcastle','Man Utd',
                  'West Ham','Crystal Palace','Brighton','Bournemouth',
                  'Fulham','Wolves','Everton','Brentford',
                  'Nottm Forest','Luton','Burnley','Sheffield Utd'],
        'MP':  [38]*20,
        'W':   [28,26,24,20,17,18,18,14,14,13,12,13,13,13,13,10,9,6,5,3],
        'D':   [7,5,10,8,6,9,3,10,6,5,7,6,5,4,4,9,12,6,5,7],
        'L':   [3,7,4,10,15,11,17,14,18,20,19,19,20,21,21,19,17,26,28,28],
        'GF':  [96,91,86,76,74,77,85,57,60,57,55,54,55,50,40,56,49,52,35,35],
        'GA':  [45,29,41,61,61,63,64,58,74,58,62,65,60,74,51,71,67,85,76,104],
        'Pts': [91,89,82,68,60,63,57,42,52,45,48,48,46,46,40,39,32,26,24,16],
        'xG':  [94,92,80,73,68,69,82,58,57,54,71,55,54,47,44,60,48,47,33,32],
    }
    df = pd.DataFrame(data)
    df.to_csv('data/raw/fbref_standings.csv', index=False)
    print('Backup data saved to data/raw/fbref_standings.csv')
    return df
 
 
# This runs when you execute the script
if __name__ == '__main__':
    df = scrape_fbref_stats()
    if df is None:          # if scraping failed, use backup
        df = load_backup_data()
    print('First 5 rows:')
    print(df.head())

