import requests
from fastapi import Request, APIRouter

from headers_util import add_niftytrader_auth_to_headers

futRouter = APIRouter()

class FutureStocks:
    def __init__(self, niftytraderauth):
        self.niftytraderauth = niftytraderauth

    async def GetAllStockFutures(self):
        url = f"https://webapi.niftytrader.in/webapi/symbol/psymbol-list"
        headers = add_niftytrader_auth_to_headers(self.niftytraderauth)

        response = requests.request("GET", url, headers=headers, data={})

        tempres = response.json()

        res = {}
        for fut in tempres['resultData']:
            res[fut['symbol_name']] = {}
            res[fut['symbol_name']]['lot_size'] = fut['lot_size']
            res[fut['symbol_name']]['max_pain'] = fut['max_pain']

        return res


@futRouter.get("/all_stocks_futures")
@futRouter.post("/all_stocks_futures")
def GetAllStockFutures(request: Request):
    url = f"https://webapi.niftytrader.in/webapi/symbol/psymbol-list"
    headers = add_niftytrader_auth_to_headers(request.headers.get('niftytraderauth'))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    return tempres['resultData']



