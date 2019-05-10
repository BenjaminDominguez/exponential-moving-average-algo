import alpaca_trade_api as trade_api
from dotenv import load_dotenv
import pandas as pd
import os

parent_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
dotenv_path = os.path.join(parent_dir, '.env')

load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get('SECRET_KEY')
KEY_ID = os.environ.get('KEY_ID')
US_TZ = 'America/New_York'

api = trade_api.REST(
    key_id=KEY_ID,
    secret_key=SECRET_KEY,
    base_url='https://paper-api.alpaca.markets/'
)

def price(symbols):
    now = pd.Timestamp.now(tz=US_TZ)
    end_dt = now

    if now.time() >= pd.Timestamp('09:30', tz=US_TZ).time():
        #If the market is open (Past 930 in the AM)
        #Get the most recent price from one minute ago
        end_dt = now - pd.Timedelta(now.strftime('%H:%M:%S') - pd.Timedelta('1 minute'))

    return _get_prices(symbols, end_dt)

def _get_prices(symbols, end_dt, max_workers=5):
    #end date is provided in func parameter
    #start date is 50 days before the end date
    start_dt = end_dt - pd.Timedelta('50 days')

    #Format to human readable dates.
    start = start_dt.strftime('%Y-%-m-%-d')
    end = end_dt.strftime('%Y-%-m-%-d')

    def get_barset(symbols):
        return api.get_barset(
            symbols,
            'day',
            limit= 50,
            start=start,
            end=end
        )

    barset = None
    idx = 0
    while idx <= len(symbols) - 1:
        if barset is None:
            #Only can make an api call for 200 symbols at a time
            barset = get_barset(symbols[idx:idx+200])
        else:
            barset.update(get_barset(symbols[idx:idx+200]))
        idx+=200
    return barset.df