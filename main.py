import pandas as pd

from bdcScraper import BDCScraper

if __name__ == '__main__':
    chrome_path = '/Users/aniruddh.agrawal/Documents/ani0/bdc-scraper/chrome/chromedriver'
    params = {
        'destinations': [{'city': 'Manali', 'state': 'Himachal Pradesh'}]
    }
    scraper = BDCScraper(params=params, chromePath=chrome_path)

    data = scraper.get_hotel_search_list(checkin='2022-04-10', checkout='2022-04-13')
    df = pd.DataFrame(data)
    df.to_csv('manali.csv', index=False)
