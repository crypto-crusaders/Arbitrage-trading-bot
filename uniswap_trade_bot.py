import time
from datetime import datetime
import json
import os.path
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

factory_contract_addr = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
pairs = []
recommend_combinations = []

MARGIN = 1.005

def log(text):
    now = datetime.now()

    # current_time = now.strftime("%Y %m %d %H:%M:%S")
    current_time = now.strftime("%H:%M:%S")
    print(f'{current_time}  {text}\n')
    print(f'this is action test project')

def console(str):
  print(f'<={str}=>')

def fetch_pairs():
  transport = AIOHTTPTransport(url=url)
  client = Client(transport=transport, fetch_schema_from_transport=True)

  query = gql("""
      query pairs {
        pairs (where: {volumeUSD_gt: 0}, orderBy: reserveUSD, orderDirection: desc, first: 1000, skip: 0 ) {
          id
          volumeUSD
          token0Price
          token1Price
          volumeToken0
          volumeToken1
          reserveUSD
          token0 {
            id
            name
            symbol
          }
          token1 {
            id
            name
            symbol
          }
          txCount
        }
      }
  """)
  
  result = client.execute(query)
  
  return result

def save_2_json ():
  result = fetch_pairs()
  json_string = json.dumps(result)

  with open('json_data.json', 'w') as outfile:
    outfile.write(json_string)

def load_from_json ():

  if os.path.isfile('./json_data.json'):
    with open('json_data.json', 'r') as json_file:
      if json_file == None:
        save_2_json ()
        load_from_json()
      else:
        global pairs
        pairs = json.load(json_file)['pairs']
  else:
    save_2_json ()
    load_from_json()
  
def get_trade_recommendations (base):

  for pair1 in pairs:
    pair1_symbol0 = pair1['token0']['symbol']
    pair1_symbol1 = pair1['token1']['symbol'];

    if pair1_symbol1 == base:
      for pair2 in pairs:

        pair2_symbol0 = pair2['token0']['symbol']
        pair2_symbol1 = pair2['token1']['symbol']

        if pair1_symbol0 == pair2_symbol1:
          
          for pair3 in pairs:
            pair3_symbol0 = pair3['token0']['symbol']
            pair3_symbol1 = pair3['token1']['symbol'];

            if pair3_symbol0 == pair2_symbol0 and pair3_symbol1 == base:
              
              recommend_combinations.append([pair1, pair2, pair3])

def compute_profit(combination):

  return float(combination[0]['token0Price']) * float(combination[1]['token0Price']) * float(combination[2]['token1Price'])
  # return 1;


def execute_trade (combination):
  # console('execute trade')
  time.sleep(1)



def uniswap_arbitrage_trade_bot():

  ticker = 'USDT'
  market = 'Uniswap'
  print(
          """
              + ============================= +
              |   AG ARBITRAGE TRADING BOT    |
              + ============================= +
              \n
          """
        )
  print('You can trade your base token with ticker {0} on exchange market - {1}. This application works by triangular arbitrage strategy. \n'.format(ticker, market))
  
  # symbols = ['WETH', 'USDT', 'USDC']

  # while(True):
    
    # fetch_tickers()
  load_from_json()

  get_trade_recommendations(ticker)

  for combination in recommend_combinations:
    profit = compute_profit(combination)
    
    title = 'triangular_arbitrage_trading'
    combination_str = f'({combination[0]["token1"]["symbol"]}-{combination[1]["token1"]["symbol"]}-{combination[2]["token0"]["symbol"]}-{combination[2]["token1"]["symbol"]})'
    desc = f'Found opportunity of profit {profit}'
    now = datetime.now()
    # if profit >= 1:
    #     desc = f'Creating buy order of profit {profit_percent}% (USDT {rate1} EARN {profit})[clock={now}]'
    # if profit <= -1:
    #     desc = f'Creating sell order of profit {profit_percent}% [clock={now}]'
    
    rate1 = 0
    
    if profit > MARGIN:
      desc = f'Creating buy order of profit {profit}% (USDT {rate1} EARN {profit})[clock={now}]'
      execute_trade(combination)

    text = title + ' - ' + combination_str + ' ' + desc

    log(text)
    time.sleep(1)

  time.sleep(1) 

uniswap_arbitrage_trade_bot()
