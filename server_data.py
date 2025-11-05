import asyncio
import csv

import uvicorn
from fastapi import FastAPI

from src.chart_router.indices import indexChartRouter
from src.chart_router.nfo import nfoChartRouter
from src.chart_router.nse import nseChartRouter
# from starlette.staticfiles import StaticFiles

# from auth.auth import authRouter
from complete_portfolio import portfolio_router
from config import master
from src.fno_marketwatch.init import fnoRouter
from src.future_stocks.init import futRouter
from src.global_indices.init import globalRouter
from src.holdings.init import holdingRouter
from src.indian_indices.init import indianRouter
from src.indian_news.init import newsRouter
from src.ipo.init import ipoRouter
from src.option_chain.init import ocRouter
from src.options.init import pcrRouter
from src.orders.init import orderRouter
from src.portfolio_analytics.init import portfolioAnalyticsRouter
from src.positions.init import positionsRouter
from src.reports.init import ledgerRouter
from src.research.init import researchRouter
from src.sectoral_indices.init import indianSectorRouter
from src.stock_corporate_actions.init import corpActionRouter
from src.stock_financials.init import finRouter
from src.stock_fundamentals.init import fundaRouter
from src.stock_marketwatch.init import trendsRouter
from src.stock_overview.init import overviewRouter
from src.stock_technicals.init import technicalRouter
from src.volume_boomers.init import volumeRouter

data_app = FastAPI()

data_app.include_router(router=portfolio_router)
data_app.include_router(router=futRouter)
data_app.include_router(router=globalRouter)
data_app.include_router(router=holdingRouter)
data_app.include_router(router=indianRouter)
data_app.include_router(router=newsRouter)
data_app.include_router(router=ocRouter)
data_app.include_router(router=pcrRouter)
data_app.include_router(router=portfolioAnalyticsRouter)
data_app.include_router(router=indianSectorRouter)
data_app.include_router(router=corpActionRouter)
data_app.include_router(router=finRouter)
data_app.include_router(router=fundaRouter)
data_app.include_router(router=overviewRouter)
data_app.include_router(router=volumeRouter)
data_app.include_router(router=technicalRouter)
data_app.include_router(router=positionsRouter)
data_app.include_router(router=orderRouter)
data_app.include_router(router=nseChartRouter)
data_app.include_router(router=nfoChartRouter)
data_app.include_router(router=indexChartRouter)
data_app.include_router(router=ledgerRouter)
data_app.include_router(router=researchRouter)
data_app.include_router(router=trendsRouter)
data_app.include_router(router=fnoRouter)
data_app.include_router(router=ipoRouter)


# Master Symbol CSV Parser
# Parses the daily master symbols file recieved from exchange and adds them to a local cache-map to save symbols against there tokens
# This is needed to prevent asking the user for token of a scrip and their ease of asking questions related to a symbol
# when the query for a symbol comes we use this map to get its token and use our APIs aacordingly
with open('master_files/NSE_symbols.txt', newline='') as csvfile:
    input_file = csv.DictReader(open("master_files/NSE_symbols.txt"))
    for row in input_file:
        master[row['Symbol']] = row['Token']
with open('master_files/NFO_symbols.txt', newline='') as csvfile:
    input_file = csv.DictReader(open("master_files/NFO_symbols.txt"))
    for row in input_file:
        master[row['TradingSymbol']] = row['Token']


async def run_data_server():
    config = uvicorn.Config(data_app, host="0.0.0.0", port=10000, loop="asyncio", lifespan="on", log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(run_data_server())
    except KeyboardInterrupt:
        pass