import time
from datetime import datetime
import pandas as pd
import ccxt

CANDLE_DURATION_IN_MIN = 5

CCXT_TICKER_NAME =  'BTC/USDT'
TRADING_TICKER_NAME = 'btcusdt'

INVESTMENT_AMOUNT_DOLLARS = 10
HOLDING_QUANTITY = 0

MARGIN = 100

exchange_names =[
    # 'binance',
    # 'bitfinex',
    # 'bittrex',
    # 'poloniex',
    # 'bitget',
    # 'bitmart',
    # 'bitvavo',
    'bitforex',
    'kuna',
]

exchange_length = len(exchange_names)

exchanges = []

def debug(term, value=None):
    print(f'<== {term} ==>\n\n', value, '\n')

def console(value):
    print(value)

for i in range(0, exchange_length):
    exchanges.append(getattr(ccxt, exchange_names[i])())

debug('all exchanges', len(ccxt.exchanges))
debug('exchanges', exchanges)

def fetch_data (ticker):
    debug('fetch', ticker)
    data = []
    for i in range(0, exchange_length):
        debug('exchange id', getattr(exchanges[i], 'id'))
        ticker_data = getattr(exchanges[i], 'fetch_ticker')(ticker)

        data.append(ticker_data)
        debug('ticker', ticker_data)
        # debug('ticker data', ticker_data['last'])
    # ticker = exchanges[0].fetch_ticker(ticker)
    # ticker = getattr(exchanges[0], 'fetch_ticker')(ticker)
    # binance = ccxt.binance()

    # ticker = binance.fetch_ticker(ticker)

    # debug('price on binance', ticker['last'])
    return data

def get_trade_recommendation(ticker_df):
    if not ticker_df or ticker_df == None or len(ticker_df) == 0:
        print(f'ticker_df should not None')
        return None

    max_ticker = min_ticker = ticker_df[0]

    for item in ticker_df:
        if item['last'] > max_ticker['last']:
            max_ticker = item
        elif item['last'] < min_ticker['last']:
            min_ticker = item

    return max_ticker, min_ticker    

def execute_trade(trade_rec_type, trading_ticker, market):
    debug('execute trade')

def run_bot_for_ticker(ccxt_ticker, trading_ticker):
    debug('run bot')
    try:
        
        ticker_data = fetch_data(ccxt_ticker)

        ticker_max, ticker_min = get_trade_recommendation(ticker_data)

        if ticker_max['last'] > ticker_min['max'] > MARGIN:
            execute_trade(ccxt_ticker, )
    except:
        print(f'error occurred while trade tokens')

run_bot_for_ticker(CCXT_TICKER_NAME, TRADING_TICKER_NAME)


# import ccxt
# import time
# binance = ccxt.binance() 
# bitfinex = ccxt.bitfinex() 
# bittrex = ccxt.bittrex() 
# poloniex = ccxt.poloniex()
# binance_ticker = binance.fetch_ticker('BTC/USDT') 
# bitfinex_ticker = bitfinex.fetch_ticker('BTC/USDT') 
# bittrex_ticker = bittrex.fetch_ticker('BTC/USDT') 
# poloniex_ticker = poloniex.fetch_ticker('BTC/USDT')
# debug('binance ticker', binance_ticker['last'])
# if binance_ticker['last'] < bitfinex_ticker['last']:
#     print("Arbitrage opportunity! Buy BTC on Binance and sell on Bitfinex.") 
# elif binance_ticker['last'] > bitfinex_ticker['last']: 
#     print("Arbitrage opportunity! Buy BTC on Bitfinex and sell on Binance.") 
# else:
#     print("No arbitrage opportunity.") 
# if binance_ticker['last'] < bittrex_ticker['last']: 
#     print("Arbitrage opportunity! Buy BTC on Binance and sell on Bittrex.") 
# elif binance_ticker['last'] > bittrex_ticker['last']:
#     print("Arbitrage opportunity! Buy BTC on Bittrex and sell on Binance.") 
# else:
#     print("No arbitrage opportunity.") 
# if binance_ticker['last'] < poloniex_ticker['last']: 
#     print("Arbitrage opportunity! Buy BTC on Binance and sell on Poloniex.") 
# elif binance_ticker['last'] > poloniex_ticker['last']:
#     print("Arbitrage opportunity! Buy BTC on Poloniex and sell on Binance.") 
# else:
#     print("No arbitrage opportunity.")