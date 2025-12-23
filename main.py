import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

BASE_URL = "https://gapi.hotmail007.com"
STOCK_API_URL = "/api/mail/getStock?mailType=outlook/hotmail/hotmail%20Trusted/outlook%20Trusted"
BUY_API_URL = "/api/mail/getMail"
CLIENT_KEY = os.getenv("CLIENT_KEY")
QUANTITY = 1  # Adjust as needed
NUM_WORKERS = 5  # Number of concurrent stock checks
CHECK_INTERVAL = 0.2  # Check every 0.2 seconds

async def check_stock(session, worker_id):
    try:
        async with session.get(STOCK_API_URL) as response:
            data = await response.json()
            stock = data.get('data', 0)
            logger.info(f"Worker {worker_id}: Stock checked - {stock}")
            return stock
    except Exception as e:
        logger.error(f"Worker {worker_id}: Error checking stock: {e}")
        return 0

async def buy_mails(session, quantity):
    try:
        params = {
            "clientKey": CLIENT_KEY,
            "mailType": "outlook/hotmail/hotmail Trusted/outlook Trusted",
            "quantity": quantity
        }
        async with session.get(BUY_API_URL, params=params) as response:
            data = await response.json()
            logger.info(f"Successfully bought {quantity} mails: {data}")
            return data
    except Exception as e:
        logger.error(f"Error buying mails: {e}")
        return None

async def worker_cycle(session, worker_id):
    while True:
        stock = await check_stock(session, worker_id)
        if stock > 0:
            logger.info(f"Worker {worker_id}: Stock available ({stock}), attempting to buy...")
            await buy_mails(session, min(QUANTITY, stock))
        await asyncio.sleep(CHECK_INTERVAL)

async def main():
    logger.info("Starting mail worker with %d concurrent workers", NUM_WORKERS)
    async with aiohttp.ClientSession(
        base_url=BASE_URL,
        connector=aiohttp.TCPConnector(limit=NUM_WORKERS * 2),  # Connection pool
        timeout=aiohttp.ClientTimeout(total=10)  # 10 second timeout
    ) as session:
        tasks = [worker_cycle(session, i) for i in range(NUM_WORKERS)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
