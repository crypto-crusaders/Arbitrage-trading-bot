import time
import json
import os.path
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

factory_contract_addr = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
pairs = []
recommend_combinations = []

LIMIT = 0

def console(str):
  print(f'<={str}=>')

def fetch_pairs():
  console(f'fetch ticker{url  }')
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
    console(f'No file')
    save_2_json ()
    load_from_json()
  
def get_trade_recommendations (base):
  #
  # 
  #

  console('get recommendations')

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
              print (f'{base} {pair1_symbol0} {pair2_symbol0} {pair3_symbol1}')
              recommend_combinations.append({
                'base': base,
                'intermediate1': pair1_symbol0,
                'intermediate2': pair2_symbol0,
                'ticker': pair2_symbol1,
              })
  console('search ended')


def compute_profit(combination):

  print('compute profit')
  return 1;


def execute_trade (combination):
  console('execute trade')

def uniswap_arbitrage_trade_bot():

  console('trading started')
  ticker = 'USDT'
  # symbols = ['WETH', 'USDT', 'USDC']

  while(True):
    
    # fetch_tickers()
    load_from_json()

    get_trade_recommendations(ticker)

    for combination in recommend_combinations:
      profit = compute_profit(combination)

      if profit > LIMIT:
        execute_trade(combination)
    # print(recommend_combinations)

    time.sleep(100000)


uniswap_arbitrage_trade_bot()