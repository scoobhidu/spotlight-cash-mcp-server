import requests
from fastapi import APIRouter, Request

from config import master, DATA_API_HOST
from headers_util import add_niftytrader_auth_to_headers, add_vensec_auth_to_headers

overviewRouter = APIRouter()

class StockOverview:
    def __init__(self, clientid, sessionid, authorization):
        self.clientid = clientid
        self.sessionid = sessionid
        self.auth = authorization

    async def GetFundamentalSummary(self, res):
        for h in res['user_portfolio']['holdings']:
            url = f"{DATA_API_HOST}/stocks/fundamental/v1/full?token={h}"
            headers = add_vensec_auth_to_headers(self.sessionid,self.clientid,self.auth)

            response = requests.request("GET", url, headers=headers, data={})

            tempres = response.json()
            res['user_portfolio']['holdings'][h]['stock_insights_summary'] = tempres['stock_Insights']
            res['user_portfolio']['holdings'][h]['stock_growth_yoy'] = tempres['prce']

    async def GetStockReturnSummary(self, res):
        for h in res['user_portfolio']['holdings']:
            url = f"{DATA_API_HOST}/stocks/fundamental/v1/returns?token={h}"
            headers = add_vensec_auth_to_headers(self.sessionid, self.clientid, self.auth)

            response = requests.request("GET", url, headers=headers, data={})

            tempres = response.json()

            for returns in tempres:
                tempres[returns] = {
                    'stock_returns': tempres[returns][0],
                    'nifty_returns': tempres[returns][1],
                }

            res['user_portfolio']['holdings'][h]['stock_returns_vs_nifty_50_index'] = tempres


@overviewRouter.get('/get_stock_overview_summary')
@overviewRouter.post('/get_stock_overview_summary')
async def GetFundamentalSummary(request: Request, symbol: str):
    url = f"{DATA_API_HOST}/stocks/fundamental/v1/full?token={master[symbol]}"
    headers = add_vensec_auth_to_headers(client_id=request.headers.get('x-client-id'), session_id=request.headers.get('session_id'), auth=request.headers.get("Authorization"))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    res = {'stock_insights_summary': tempres['stock_Insights'], 'stock_growth_yoy': tempres['prce']}

    return res

@overviewRouter.get('/get_stock_returns_summary')
@overviewRouter.post('/get_stock_returns_summary')
async def GetStockReturnSummary(request: Request, symbol: str):
    url = f"{DATA_API_HOST}/stocks/fundamental/v1/returns?token={master[symbol]}"
    headers = add_vensec_auth_to_headers(client_id=request.headers.get('x-client-id'), session_id=request.headers.get('session_id'), auth=request.headers.get("Authorization"))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    for returns in tempres:
        tempres[returns] = {
            'stock_returns': tempres[returns][0],
            'nifty_returns': tempres[returns][1],
        }

    return {'stock_returns_vs_nifty_50_index': tempres}

