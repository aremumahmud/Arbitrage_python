const ccxt = require('ccxt');
const binance_api_key = 'zphzNsRpLatgdc0N8iolzjFWr7qbXSaE8CLAIbg9XrKT6QzW0orzan7klz16LEEC'
const binance_api_secret = 'M35tAkINeuMELayPTmBRrtj2HJQokoBvdMaJVhqq9rGHogEzbnpcN2sHfrykvlnx'

async function runArbitrage() {
    const binance = new ccxt.binance({
        apiKey: binance_api_key,
        secret: binance_api_secret,
    });

    const symbol = 'ETH/USDT';
    const usdtAmount = 50;
    const targetProfit = 0.5;

    try {
        // Fetch the current ticker for the trading pair
        const ticker = await binance.fetchTicker(symbol);

        // Calculate the equivalent ETH you can buy with the USDT amount
        const ethAmount = usdtAmount / ticker.last;

        // Place a buy order to convert USDT to ETH
        const buyOrder = await binance.createMarketBuyOrder(symbol, ethAmount);

        // Check the response of the buy order and handle errors if any
        if (buyOrder.hasOwnProperty('id')) {
            // Buy order successful, ETH acquired
            const ethBought = buyOrder.filled;

            let profit = 0;

            while (profit < targetProfit) {
                // Fetch the current ticker for the trading pair
                const updatedTicker = await binance.fetchTicker(symbol);

                // Calculate the current profit based on the updated ticker
                const currentProfit = (updatedTicker.last * ethBought) - usdtAmount;

                if (currentProfit >= targetProfit) {
                    // Place a sell order to convert ETH back to USDT
                    const sellOrder = await binance.createMarketSellOrder(symbol, ethBought);

                    // Check the response of the sell order and handle errors if any
                    if (sellOrder.hasOwnProperty('id')) {
                        // Sell order successful, USDT acquired
                        const usdtAcquired = sellOrder.filled * updatedTicker.last;
                        profit = usdtAcquired - usdtAmount;
                        console.log(`Profit: ${profit} USDT`);
                    } else {
                        console.log('Sell order failed');
                    }
                }

                // Wait for a certain interval before polling again
                await sleep(5000); // 5 seconds
            }
        } else {
            console.log('Buy order failed');
        }
    } catch (error) {
        console.error('An error occurred:', error.message);
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

runArbitrage();