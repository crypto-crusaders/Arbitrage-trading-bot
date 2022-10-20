import time
from datetime import datetime
import pandas as pd
import numpy as np
# from wazirx_sapi_client.rest import Client
import ccxt
# import talib
# from config import wazirx_config

# Initialize Variables
CANDLE_DURATION_IN_MIN = 5

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

CCXT_TICKER_NAME = 'BTC/USDT'
TRADING_TICKER_NAME = 'btcusdt'

INVESTMENT_AMOUNT_DOLLARS = 10
HOLDING_QUANTITY = 0

exchange = ccxt.binance()
# wx_client = Client(api_key=wazirx_config.API_KEY, secret_key=wazirx_config.API_SECRET)

# STEP 1: FETCH THE DATA
def fetch_data(ticker):
    global exchange
    bars,ticker_df = None, None

    try:
        bars = exchange.fetch_ohlcv(ticker, timeframe=f'{CANDLE_DURATION_IN_MIN}m', limit=100)
    except:
        print(f"Error in fetching data from the exchange:{ticker}")

    if bars is not None:
        ticker_df = pd.DataFrame(bars[:-1], columns=['at', 'open', 'high', 'low', 'close', 'vol'])
        ticker_df['Date'] = pd.to_datetime(ticker_df['at'], unit='ms')
        ticker_df['symbol'] = ticker

    return ticker_df

# # STEP 2: COMPUTE THE TECHNICAL INDICATORS & APPLY THE TRADING STRATEGY
# def get_trade_recommendation(ticker_df):

#     macd_result = 'WAIT'
#     final_result = 'WAIT'

#     # BUY or SELL based on MACD crossover points and the RSI value at that point
#     macd, signal, hist = talib.MACD(ticker_df['close'], fastperiod = 12, slowperiod = 26, signalperiod = 9)
#     last_hist = hist.iloc[-1]
#     prev_hist = hist.iloc[-2]
#     if not np.isnan(prev_hist) and not np.isnan(last_hist):
#         # If hist value has changed from negative to positive or vice versa, it indicates a crossover
#         macd_crossover = (abs(last_hist + prev_hist)) != (abs(last_hist) + abs(prev_hist))
#         if macd_crossover:
#             macd_result = 'BUY' if last_hist > 0 else 'SELL'

#     if macd_result != 'WAIT':
#         rsi = talib.RSI(ticker_df['close'], timeperiod = 14)
#         # Consider last 3 RSI values
#         last_rsi_values = rsi.iloc[-3:]

#         if (last_rsi_values.min() <= RSI_OVERSOLD):
#             final_result = 'BUY'
#         elif (last_rsi_values.max() >= RSI_OVERBOUGHT):
#             final_result = 'SELL'

#     return final_result


# # STEP 3: EXECUTE THE TRADE
# def execute_trade(trade_rec_type, trading_ticker):
#     global wx_client, HOLDING_QUANTITY
#     order_placed = False
#     side_value = 'buy' if (trade_rec_type == "BUY") else 'sell'
#     try:
#         ticker_price_response = wx_client.send("ticker", { "symbol": trading_ticker})
#         if (ticker_price_response[0] in [200, 201]):
#             current_price = float(ticker_price_response[1]['lastPrice'])

#             scrip_quantity = round(INVESTMENT_AMOUNT_DOLLARS/current_price,5) if trade_rec_type == "BUY" else HOLDING_QUANTITY
#             print(f"PLACING ORDER {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: "
#                   f"{trading_ticker}, {side_value}, {current_price}, {scrip_quantity}, {int(time.time() * 1000)} ")

#             order_response = wx_client.send("create_order",
#                                         {"symbol": trading_ticker, "side": side_value, "type": "limit",
#                                          "price": current_price, "quantity": scrip_quantity,
#                                          "recvWindow": 10000, "timestamp": int(time.time() * 1000)})

#             print(f"ORDER PLACED")
#             HOLDING_QUANTITY = scrip_quantity if trade_rec_type == "BUY" else HOLDING_QUANTITY
#             order_placed = True
#     except:
#         print(f"\nALERT!!! UNABLE TO COMPLETE ORDER")

#     return order_placed


def run_bot_for_ticker(ccxt_ticker, trading_ticker):

#     currently_holding = False
    while 1:
        # STEP 1: FETCH THE DATA
        ticker_data = fetch_data(ccxt_ticker)
#         if ticker_data is not None:
#             # STEP 2: COMPUTE THE TECHNICAL INDICATORS & APPLY THE TRADING STRATEGY
#             trade_rec_type = get_trade_recommendation(ticker_data)
#             print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}  TRADING RECOMMENDATION: {trade_rec_type}')

#             # STEP 3: EXECUTE THE TRADE
#             if (trade_rec_type == 'BUY' and not currently_holding) or \
#                 (trade_rec_type == 'SELL' and currently_holding):
#                 print(f'Placing {trade_rec_type} order')
#                 trade_successful = execute_trade(trade_rec_type,trading_ticker)
#                 currently_holding = not currently_holding if trade_successful else currently_holding

#             time.sleep(CANDLE_DURATION_IN_MIN*60)
#         else:
#             print(f'Unable to fetch ticker data - {ccxt_ticker}. Retrying!!')
#             time.sleep(5)

        time.sleep(1)
        
run_bot_for_ticker(CCXT_TICKER_NAME,TRADING_TICKER_NAME)

import ccxt
import time
binance = ccxt.binance() 
# bitfinex = ccxt.bitfinex() 
# bittrex = ccxt.bittrex() 
# poloniex = ccxt.poloniex()
binance_ticker = binance.fetch_ticker('BTC/USDT') 
# bitfinex_ticker = bitfinex.fetch_ticker('BTC/USDT') 
# bittrex_ticker = bittrex.fetch_ticker('BTC/USDT') 
# poloniex_ticker = poloniex.fetch_ticker('BTC/USDT')
print(binance_ticker['last'])
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

