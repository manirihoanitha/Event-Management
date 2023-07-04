from decimal import Decimal
import requests


def add_commas(number):
    return '{:,.2f}'.format(number)


def convert_usd_to_rwf(usd):
    url = f"https://v6.exchangerate-api.com/v6/d13b9c45debb8c44f465bad6/pair/USD/RWF"
    try:
        response = requests.get(url)
        response.raise_for_status()  # raise exception if the request failed
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching exchange rate: {e}")
        return None  # you may want to handle this in a different way

    data = response.json()
    if data.get('result') == 'error':
        print("Unable to find exchange rate in API response")
        return None  # again, handle this case as appropriate for your application

    rate = Decimal(data['conversion_rate'])
    rwf = usd * rate
    # rounding to 2 decimal places and adding commas
    return add_commas(round(rwf, 2))
