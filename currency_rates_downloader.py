import requests
import pandas as pd
from datetime import datetime, timedelta
import configparser

class Extractor:
    def __init__(self, currency, single_date, bank):
        self.currency = currency
        self.single_date = single_date
        self.bank = bank

    def fetch_data(self):
        if self.bank == "nbrb":
            return self.fetch_from_nbrb()
        elif self.bank == "cbu":
            return self.fetch_from_cbu()
        else:
            raise ValueError(f"Unsupported bank setting: {self.bank}")

    def fetch_from_nbrb(self):
        url_date_str = self.single_date.strftime("%Y-%m-%d")
        url = f"https://api.nbrb.by/exrates/rates/{self.currency}?parammode=2&ondate={url_date_str}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                return {
                    'Date': self.single_date.strftime("%d.%m.%Y"),
                    'Rate': data.get('Cur_OfficialRate'),
                    'Currency': self.currency,
                    'BaseNominal': data.get('Cur_Scale'),
                    'BaseCurrency': 'BYN'
                }
        return None

    def fetch_from_cbu(self):
        url_date_str = self.single_date.strftime("%Y-%m-%d")
        url = f"https://cbu.uz/ru/arkhiv-kursov-valyut/json/{self.currency}/{url_date_str}/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return {
                    'Date': self.single_date.strftime("%d.%m.%Y"),
                    'Rate': data[0]['Rate'],
                    'Currency': self.currency,
                    'BaseNominal': 1,
                    'BaseCurrency': 'UZS'
                }
        return None

class Downloader:
    def __init__(self, currencies, start_date, end_date, bank):
        self.currencies = currencies
        self.start_date = start_date
        self.end_date = end_date
        self.bank = bank
        self.final_data = []

    def collect_data(self):
        date_range = [self.start_date + timedelta(days=x) for x in range((self.end_date - self.start_date).days + 1)]
        for currency in self.currencies:
            print(f"Fetching data for currency: {currency}")
            for single_date in date_range:
                extractor = Extractor(currency, single_date, self.bank)
                data = extractor.fetch_data()

                if data:
                    self.final_data.append(data)
                else:
                    self.final_data.append({
                        'Date': single_date.strftime("%d.%m.%Y"),
                        'Rate': None,
                        'Currency': currency,
                        'BaseNominal': None,
                        'BaseCurrency': 'UNKNOWN'
                    })

    def save_to_excel(self, filename):
        final_df = pd.DataFrame(self.final_data)
        final_df = final_df[['Date', 'Rate', 'Currency', 'BaseNominal', 'BaseCurrency']]
        final_df.to_excel(filename, index=False)
        print(f"Data saved to {filename}")

def main():
    # Read configuration from the .ini file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get the days_to_fetch, currencies, and bank from the config
    days_to_fetch = config.getint('settings', 'days_to_fetch')
    currencies = config.get('settings', 'currencies').split(', ')
    bank = config.get('settings', 'bank').strip()

    # Get the end_date from the config, or use today's date if not provided
    end_date_str = config.get('settings', 'end_date', fallback=None)
    if end_date_str:
        end_date = datetime.strptime(end_date_str.split(';')[0].strip(), "%Y-%m-%d")
    else:
        end_date = datetime.now()

    start_date = end_date - timedelta(days=days_to_fetch)

    # Initialize Downloader and collect data
    downloader = Downloader(currencies, start_date, end_date, bank)
    downloader.collect_data()

    # Create a filename and save the data
    filename = f"{bank}_currency_data_{start_date.strftime('%Y-%m-%d')}_to_{end_date.strftime('%Y-%m-%d')}.xlsx"
    downloader.save_to_excel(filename)

if __name__ == "__main__":
    main()
