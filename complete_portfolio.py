from fastapi import APIRouter, Request

from config import nifty_trader_auth
from src.future_stocks.init import FutureStocks
from src.holdings.init import UserHoldings

portfolio_router = APIRouter()

@portfolio_router.get("/fetch_complete_portfolio")
@portfolio_router.post("/fetch_complete_portfolio")
async def read_item(request: Request):
    clientid = request.headers.get('x-client-id')
    authorization = request.headers.get('Authorization')
    sessionid = request.headers.get('session_id')

    holdings = UserHoldings(clientid=clientid, authorization=authorization, sessionid=sessionid)
    fut_stocks_list = FutureStocks(niftytraderauth=nifty_trader_auth)

    futlist = await fut_stocks_list.GetAllStockFutures()

    response = {'user_portfolio': await holdings.GetHoldings(futlist)}

    return response