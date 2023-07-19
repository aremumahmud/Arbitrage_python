const ccxt = require('ccxt');

async function runArbitrage() {
  const binance = new ccxt.binance({
    apiKey: 'YOUR_API_KEY',
    secret: 'YOUR_API_SECRET',
  });

  const symbol = 'ETH/USDT';
  const usdtAmount = 50;
  const targetProfit = 0.5;
  let firstBuyPrice = null;

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

      if (!firstBuyPrice) {
        firstBuyPrice = ticker.last;
        console.log('First buying price:', firstBuyPrice);
      } else {
        const currentPrice = ticker.last;
        const priceDifference = currentPrice - firstBuyPrice;

        if (Math.abs(priceDifference) <= targetProfit) {
          // Place a sell order to convert ETH back to USDT
          const sellOrder = await binance.createMarketSellOrder(symbol, ethBought);

          // Check the response of the sell order and handle errors if any
          if (sellOrder.hasOwnProperty('id')) {
            // Sell order successful, USDT acquired
            const usdtAcquired = sellOrder.filled * ticker.last;
            const profit = usdtAcquired - usdtAmount;
            console.log(`Profit: ${profit} USDT`);
          } else {
            console.log('Sell order failed');
          }
        }
      }
    } else {
      console.log('Buy order failed');
    }
  } catch (error) {
    console.error('An error occurred:', error.message);
  }
}

setInterval(runArbitrage, 10000); // Run every 10 seconds

runArbitrage(); // Run immediately

