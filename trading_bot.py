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

# exchange_id = 'kuna'
exchange_id = 'binance'

exchange = None

def debug(term, value=None):
    print(f'<== {term} ==>\n\n', value, '\n')

def console(value):
    print(value)

def log(text):
    now = datetime.now()

    # current_time = now.strftime("%Y %m %d %H:%M:%S")
    current_time = now.strftime("%H:%M:%S")
    print(f'{current_time}  {text}\n')

def fetch_current_ticker_price(ticker):
    debug('fetch ticker price')

def check_profit_loss(total_price_after_sell,initial_investment,transaction_brokerage, min_profit):
    apprx_brokerage = transaction_brokerage * initial_investment/100 * 3
    min_profitable_price = initial_investment + apprx_brokerage + min_profit
    profit_loss = round(total_price_after_sell - min_profitable_price,3)
    return profit_loss

def fetch_market_data(id):
    exchange = getattr(ccxt, id)()

    markets = exchange.load_markets()

    return sorted(markets.items()), sorted(markets)
    # return markets

def fetch_ticker(ticker, id):
    exchange = getattr(ccxt, id)()

    return exchange.fetch_ticker(ticker)
    
def get_rate_for_ticker(ticker):
    data = exchange.fetch_ticker(ticker)
    return data
def get_profit_loss(sym1, sym2, sym3):

    rate1 = fetch_ticker(sym1, exchange_id)['ask']
    rate2 = fetch_ticker(sym2, exchange_id)['ask']
    rate3 = fetch_ticker(sym3, exchange_id)['ask']

    profit = (rate1 * rate2 - rate3)
    profit_percent = profit / rate3 if rate3 > 0 else 0   
    

    return profit, profit_percent, rate1

def get_trade_recommendation(tickers, base):

    combinations = []

    for sym1 in tickers:   
        sym1_token1 = sym1.split('/')[0]
        sym1_token2 = sym1.split('/')[1]   
        if (sym1_token2 == base):
            for sym2 in tickers:
                sym2_token1 = sym2.split('/')[0]
                sym2_token2 = sym2.split('/')[1]
                if (sym1_token1 == sym2_token2):
                    for sym3 in tickers:
                        sym3_token1 = sym3.split('/')[0]
                        sym3_token2 = sym3.split('/')[1]
                        if((sym2_token1 == sym3_token1) and (sym3_token2 == sym1_token2)):
                            
                            profit, profit_percent, rate1 = get_profit_loss(sym1, sym2, sym3)

                            combination = {
                                'base':sym1_token2,
                                'intermediate':sym1_token1,
                                'ticker':sym2_token1,
                            }
                            
                            title = 'triangular_arbitrage_trading'
                            combination_str = f'({combination["base"]}-{combination["intermediate"]}-{combination["ticker"]}-{combination["base"]})'
                            desc = f'Found opportunity of profit {profit_percent}%'
                            now = datetime.now()
                            if profit >= 1:
                                desc = f'Creating buy order of profit {profit_percent}% (USDT {rate1} EARN {profit})[clock={now}]'
                            if profit <= -1:
                                desc = f'Creating sell order of profit {profit_percent}% [clock={now}]'
                            
                            text = title + ' - ' + combination_str + ' ' + desc

                            log(text)
                            combinations.append(combination)
    return combinations

def execute_trade(trade_rec_type, trading_ticker, market):
    debug('execute trade')

def display_title():
    print(
        """
            + ============================= +
            |   AG ARBITRAGE TRADING BOT    |
            + ============================= +
            \n
        """)
    print('You can trade your base token with ticker {0} on exchange market - {1}. This application works by triangular arbitrage strategy. \n'.format(CCXT_TICKER_NAME, exchange_id))
def run_bot_for_ticker(ccxt_ticker, trading_ticker):
    print(datetime.now())
    display_title()

    while True:
        markets, tickers = fetch_market_data(exchange_id)
        
        ticker_df = fetch_ticker(ccxt_ticker, exchange_id)


        combinations = get_trade_recommendation(tickers, 'USDT')


        execute_trade('', ccxt_ticker, exchange_id)

run_bot_for_ticker(CCXT_TICKER_NAME, TRADING_TICKER_NAME)
