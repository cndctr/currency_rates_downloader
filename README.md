# Currency Data Fetcher

This script fetches historical currency exchange rates from specified banks (NBRB and CBU) and saves the data to an Excel file. It allows users to configure which currencies to retrieve, the date range, and the source bank through a configuration file.

## Features

- Fetches exchange rates for multiple currencies over a specified date range.
- Supports data retrieval from two banks: the National Bank of the Republic of Belarus (NBRB) and the Central Bank of Uzbekistan (CBU).
- Outputs the collected data to an Excel file.

## Requirements

- Python 3.x
- Libraries:
  - `requests`
  - `pandas`
  - `configparser`
  
You can install the required libraries using pip:

```bash
pip install requests pandas
```

## Configuration

The script uses a configuration file named `config.ini`. Here’s the expected format:

```ini
[settings]
days_to_fetch = 30
currencies = USD, EUR, RUB
bank = nbrb
end_date = 2024-11-01
```

- **days_to_fetch**: Number of days to fetch data for (integer).
- **currencies**: A comma-separated list of currency codes (e.g., `USD, EUR, RUB`).
- **bank**: The source bank for data retrieval. Choose either `nbrb` or `cbu`.
- **end_date**: The end date for the data collection in `YYYY-MM-DD` format (optional; defaults to today if not provided).

## Usage

1. Configure the `config.ini` file with the desired settings.
2. Run the script:

```bash
python currency_data_fetcher.py
```

3. The output will be an Excel file named in the format `{bank}_currency_data_{start_date}_to_{end_date}.xlsx`, saved in the current working directory.

## Example

To fetch exchange rates for USD and EUR from the NBRB over the last 30 days, your `config.ini` should look like this:

```ini
[settings]
days_to_fetch = 30
currencies = USD, EUR
bank = nbrb
```

After running the script, you'll find the exchange rates saved in an Excel file named something like `nbrb_currency_data_2024-10-02_to_2024-11-01.xlsx`.

## License

This project is open-source and available under the MIT License. Feel free to modify and distribute as per the license terms.
