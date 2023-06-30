import ccxt

# Connect to Binance
binance_api_key = ' '
binance_api_secret = ' '
binance_exchange = ccxt.binance({
    'apiKey': binance_api_key,
    'secret': binance_api_secret
})

# Connect to KuCoin
kucoin_api_key = ' '
kucoin_api_secret = ' '
kucoin_exchange = ccxt.kucoin({
    'apiKey': kucoin_api_key,
    'secret': kucoin_api_secret
})

# Function to compare prices and perform arbitrage
def perform_arbitrage():
    # Get price information from both exchanges
    binance_ticker = binance_exchange.fetch_ticker('BTC/USDT')
    kucoin_ticker = kucoin_exchange.fetch_ticker('BTC/USDT')

    # Extract prices from the ticker data
    binance_price = binance_ticker['last']
    kucoin_price = kucoin_ticker['last']

    # Compare prices and perform arbitrage if conditions are met
    if binance_price > kucoin_price + 1.5:
        # Buy $50 worth of BTC on KuCoin
        kucoin_amount = 50 / kucoin_price
        kucoin_order = kucoin_exchange.create_market_buy_order('BTC/USDT', kucoin_amount)

        # Send the bought BTC to Binance
        binance_address = binance_exchange.fetch_deposit_address('BTC')
        binance_withdrawal = binance_exchange.withdraw('BTC', kucoin_amount, binance_address['address'])

        print('Arbitrage opportunity found and executed!')
        print('Bought BTC on KuCoin:', kucoin_order)
        print('Sent BTC to Binance:', binance_withdrawal)
    else:
        print('No arbitrage opportunity found.')

# Perform arbitrage
perform_arbitrage()
