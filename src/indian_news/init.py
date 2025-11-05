import requests
from fastapi import APIRouter, Request

from config import DATA_API_HOST
from headers_util import add_niftytrader_auth_to_headers, add_vensec_auth_to_headers

newsRouter = APIRouter()

class IndianNews:
    def __init__(self, clientid, sessionid, authorization, niftytraderauth, symbol):
        self.clientid = clientid
        self.sessionid = sessionid
        self.auth = authorization

        self.symbol = symbol

        self.niftytraderauth = niftytraderauth

    async def Get10LatestNewsSummary(self):
        url = f"https://webapi.niftytrader.in/webapi/Other/ai-news-pagination?category=India&pageNumber=1&pageSize=10"
        headers = add_niftytrader_auth_to_headers(self.niftytraderauth)

        response = requests.request("GET", url, headers=headers, data={})

        return response.json()

    async def GetLatestStockNews(self):
        url = f"{DATA_API_HOST}/news/v2/stockdetails/summary"
        payload = f'{"start_dt":"","end_dt":"","sym":"{self.symbol}","limit":10,"page":0}'
        headers = add_vensec_auth_to_headers(self.sessionid,self.clientid,self.auth)

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()

@newsRouter.get('/get_20_latest_news_summary')
@newsRouter.post('/get_20_latest_news_summary')
async def Get10LatestNewsSummary(request: Request):
    url = f"https://webapi.niftytrader.in/webapi/Other/ai-news-pagination?category=India&pageNumber=1&pageSize=20"
    headers = add_niftytrader_auth_to_headers(request.headers.get('niftytraderauth'))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    del tempres['result']
    del tempres['resultMessage']
    del tempres['resultData']['totalItems']
    del tempres['resultData']['maxNavigationPages']
    del tempres['resultData']['pageNumber']
    del tempres['resultData']['pageSize']
    del tempres['resultData']['totalPages']
    del tempres['resultData']['startPage']
    del tempres['resultData']['endPage']
    del tempres['resultData']['pageNumbers']

    return tempres

@newsRouter.get('/get_10_latest_stock_news_summary')
@newsRouter.post('/get_10_latest_stock_news_summary')
async def GetLatestStockNews(request: Request, symbol: str):
    url = f"{DATA_API_HOST}/news/v2/stockdetails/summary"
    payload = '{"start_dt":"", "end_dt":"", "sym": "' + symbol + '", "limit":10, "page":0}'
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'),request.headers.get('x-client-id'),request.headers.get('Authorization'))

    response = requests.request("POST", url, headers=headers, data=payload)

    tempres = response.json()

    del tempres['page']
    del tempres['size']
    del tempres['total']

    for news in tempres['data']:
        del news['b_img']
        del news['n_id']

    return tempres


