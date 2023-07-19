import ccxt
import time

def run_arbitrage():
   # Connect to Binance and KuCoin
    binance_api_key = 'zphzNsRpLatgdc0N8iolzjFWr7qbXSaE8CLAIbg9XrKT6QzW0orzan7klz16LEEC'
    binance_api_secret = 'M35tAkINeuMELayPTmBRrtj2HJQokoBvdMaJVhqq9rGHogEzbnpcN2sHfrykvlnx'
    binance = ccxt.binance({
        'apiKey': binance_api_key,
        'secret': binance_api_secret
    })

    symbol = 'ETH/USDT'
    usdt_amount = 50
    target_profit = 0.5

    try:
        # Fetch the current ticker for the trading pair
        ticker = binance.fetch_ticker(symbol)

        # Calculate the equivalent ETH you can buy with the USDT amount
        eth_amount = usdt_amount / ticker['last']

        # Place a buy order to convert USDT to ETH
        buy_order = binance.create_market_buy_order(symbol, eth_amount)

        # Check the response of the buy order and handle errors if any
        if 'id' in buy_order:
            # Buy order successful, ETH acquired
            eth_bought = buy_order['filled']

            profit = 0

            while profit < target_profit:
                # Fetch the current ticker for the trading pair
                updated_ticker = binance.fetch_ticker(symbol)

                # Calculate the current profit based on the updated ticker
                current_profit = (updated_ticker['last'] * eth_bought) - usdt_amount

                if current_profit >= target_profit:
                    # Place a sell order to convert ETH back to USDT
                    sell_order = binance.create_market_sell_order(symbol, eth_bought)

                    # Check the response of the sell order and handle errors if any
                    if 'id' in sell_order:
                        # Sell order successful, USDT acquired
                        usdt_acquired = sell_order['filled'] * updated_ticker['last']
                        profit = usdt_acquired - usdt_amount
                        print(f"Profit: {profit} USDT")
                    else:
                        print('Sell order failed')

                # Wait for a certain interval before polling again
                time.sleep(5)  # 5 seconds

        else:
            print('Buy order failed')
    except Exception as e:
        print('An error occurred:', str(e))

run_arbitrage()
