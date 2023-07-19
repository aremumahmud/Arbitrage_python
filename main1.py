import ccxt
import concurrent.futures
import time

# Define the list of trading pairs to perform arbitrage on
trading_pairs = ['BTC/USDT', 'ETH/USDT', 'ETH/BTC', 'LTC/USDT', 'LTC/BTC', 'XRP/USDT', 'XRP/BTC', 'ADA/USDT', 'ADA/BTC', 'DOT/USDT', 'DOT/BTC', 'LINK/USDT', 'LINK/BTC', 'BNB/USDT', 'BNB/BTC', 'DOGE/USDT', 'DOGE/BTC', 'XLM/USDT', 'XLM/BTC', 'UNI/USDT']


# Connect to Binance and KuCoin
binance_api_key = 'zphzNsRpLatgdc0N8iolzjFWr7qbXSaE8CLAIbg9XrKT6QzW0orzan7klz16LEEC'
binance_api_secret = 'M35tAkINeuMELayPTmBRrtj2HJQokoBvdMaJVhqq9rGHogEzbnpcN2sHfrykvlnx'
binance_exchange = ccxt.binance({
    'apiKey': binance_api_key,
    'secret': binance_api_secret
})

kucoin_api_key = '6494c448e93c7c0001c7cb57'
kucoin_api_secret = '18efa545-0e61-431b-a093-58a3e588090d'
kucoin_exchange = ccxt.kucoin({
    'apiKey': kucoin_api_key,
    'secret': kucoin_api_secret
})

# Function to compare prices and perform arbitrage for a single pair
def perform_arbitrage(pair):
    # Get price information from both exchanges for the given pair
    binance_ticker = binance_exchange.fetch_ticker(pair)
    kucoin_ticker = kucoin_exchange.fetch_ticker(pair)

    # Extract prices from the ticker data
    binance_price = binance_ticker['last']
    kucoin_price = kucoin_ticker['last']
    #print('(Binance > KuCoin)',pair,binance_price,kucoin_price)
    # Compare prices and perform arbitrage if conditions are met
    if binance_price > kucoin_price + 0.1:
        kucoin_amount = 50 / kucoin_price
        # kucoin_order = kucoin_exchange.create_market_buy_order(pair, kucoin_amount)

        # binance_address = binance_exchange.fetch_deposit_address('BTC')
        # binance_withdrawal = binance_exchange.withdraw('BTC', kucoin_amount, binance_address['address'])

        print('Arbitrage opportunity found (Binance > KuCoin) for', pair)
        # print('Bought', pair.split('/')[0], 'on KuCoin:', kucoin_order)
        # print('Sent', pair.split('/')[0], 'to Binance:', binance_withdrawal)
    elif kucoin_price > binance_price + 0.1:
        binance_amount = 50 / binance_price
        # binance_order = binance_exchange.create_market_buy_order(pair, binance_amount)

        # kucoin_address = kucoin_exchange.fetch_deposit_address('BTC')
        # kucoin_withdrawal = kucoin_exchange.withdraw('BTC', binance_amount, kucoin_address['address'])

        print('Arbitrage opportunity found (KuCoin > Binance) for', pair)
        # print('Bought', pair.split('/')[0], 'on Binance:', binance_order)
        # print('Sent', pair.split('/')[0], 'to KuCoin:', kucoin_withdrawal)
    else:
        hello = 66

# Create thread pool and map the perform_arbitrage function to each pair
while True:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(perform_arbitrage, trading_pairs)
    time.sleep(1)
    #executor.map(perform_arbitrage, trading_pairs)
