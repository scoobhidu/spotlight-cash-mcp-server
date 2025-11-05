import requests
from fastapi import APIRouter, Request

from config import master, DATA_API_HOST
from headers_util import add_vensec_auth_to_headers

technicalRouter = APIRouter()

class StockTechnicals:
    def __init__(self, clientid, sessionid, authorization):
        self.clientid = clientid
        self.sessionid = sessionid
        self.auth = authorization

    async def GetStockSMA(self, res):
        for h in res['user_portfolio']['holdings']:
            url = f"{DATA_API_HOST}/stocks/v2/sma?token={h}&exch=NSE"
            headers = add_vensec_auth_to_headers(self.sessionid,self.clientid,self.auth)

            response = requests.request("GET", url, headers=headers, data={})

            tempres = response.json()

            if 'technicals' not in res['user_portfolio']['holdings'][h]:
                res['user_portfolio']['holdings'][h]['technicals'] = {}

            res['user_portfolio']['holdings'][h]['technicals']['simple_moving_average'] = tempres


    async def GetPivot(self, res):
        for h in res['user_portfolio']['holdings']:
            url = f"{DATA_API_HOST}/stocks/v2/technical?token={h}"
            headers = add_vensec_auth_to_headers(self.sessionid,self.clientid,self.auth)

            response = requests.request("GET", url, headers=headers, data={})

            tempres = response.json()

            if 'technicals' not in res['user_portfolio']['holdings'][h]:
                res['user_portfolio']['holdings'][h]['technicals'] = {}

            res['user_portfolio']['holdings'][h]['technicals']['pivots'] = {
                'resistance_3': tempres['r3'],
                'resistance_2': tempres['r2'],
                'resistance_1': tempres['r1'],
                'pivot': tempres['pivot'],
                'support_1': tempres['s1'],
                'support_2': tempres['s2'],
                'support_3': tempres['s3'],
            }


@technicalRouter.get('/get_stock_simple_moving_average')
@technicalRouter.post('/get_stock_simple_moving_average')
async def GetStockSMA(request: Request, symbol: str):
    url = f"{DATA_API_HOST}/stocks/v2/sma?token={master[symbol]}&exch=NSE"
    headers = add_vensec_auth_to_headers(client_id=request.headers.get('x-client-id'),
                                         session_id=request.headers.get('session_id'),
                                         auth=request.headers.get("Authorization"))

    response = requests.request("GET", url, headers=headers, data={})

    return response.json()


@technicalRouter.get('/get_stock_pivots')
@technicalRouter.post('/get_stock_pivots')
async def GetPivot(request: Request, symbol: str):
    url = f"{DATA_API_HOST}/stocks/v2/technical?token={master[symbol]}"
    headers = add_vensec_auth_to_headers(client_id=request.headers.get('x-client-id'),
                                         session_id=request.headers.get('session_id'),
                                         auth=request.headers.get("Authorization"))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    return {
        'resistance_3': tempres['r3'],
        'resistance_2': tempres['r2'],
        'resistance_1': tempres['r1'],
        'pivot': tempres['pivot'],
        'support_1': tempres['s1'],
        'support_2': tempres['s2'],
        'support_3': tempres['s3'],
    }

