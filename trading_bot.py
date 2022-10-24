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

def debug(term, value=None):
    print(f'<== {term} ==>\n\n', value, '\n')

def console(value):
    print(value)

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

def get_trade_recommendation(tickers, base):
    print('get trade recommendation')

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
                            combination = {
                                'base':sym1_token2,
                                'intermediate':sym1_token1,
                                'ticker':sym2_token1,
                            }
                            combinations.append(combination)
    return combinations

def execute_trade(trade_rec_type, trading_ticker, market):
    debug('execute trade')

def run_bot_for_ticker(ccxt_ticker, trading_ticker):

    markets, tickers = fetch_market_data(exchange_id)

    debug('tickers', tickers)

    combinations = get_trade_recommendation(tickers, 'USDT')

    debug('combinations', combinations)

    execute_trade('', ccxt_ticker, exchange_id)

run_bot_for_ticker(CCXT_TICKER_NAME, TRADING_TICKER_NAME)
