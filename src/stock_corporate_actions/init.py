import requests
from fastapi import APIRouter, Request

from config import master, DATA_API_HOST
from headers_util import add_vensec_auth_to_headers

corpActionRouter = APIRouter()

class StockCorporateActions:
    def __init__(self, clientid, sessionid, authorization):
        self.clientid = clientid
        self.sessionid = sessionid
        self.auth = authorization

    async def GetCorporateActions(self, res):
        for h in res['user_portfolio']['holdings']:
            url = f"{DATA_API_HOST}/stocks/fundamental/v1/corpaction?token={h}"
            headers = add_vensec_auth_to_headers(self.sessionid,self.clientid,self.auth)

            response = requests.request("GET", url, headers=headers, data={})
            tempres = response.json()

            if 'corporate_actions' not in res['user_portfolio']['holdings'][h]:
                res['user_portfolio']['holdings'][h]['corporate_actions'] = {}

            res['user_portfolio']['holdings'][h]['corporate_actions']['splits'] = tempres


    async def GetDividends(self, res):
        for h in res['user_portfolio']['holdings']:
            url = f"{DATA_API_HOST}/stocks/fundamental/v1/dividend?token={h}"
            headers = add_vensec_auth_to_headers(self.sessionid,self.clientid,self.auth)

            response = requests.request("GET", url, headers=headers, data={})
            tempres = response.json()

            if 'corporate_actions' not in res['user_portfolio']['holdings'][h]:
                res['user_portfolio']['holdings'][h]['corporate_actions'] = {}

            for t in tempres:
                t['dividend_percentage'] = t['perc']
                del t['perc']

            res['user_portfolio']['holdings'][h]['corporate_actions']['dividends'] = tempres

    async def GetBoardAnnouncements(self, res):
        for h in res['user_portfolio']['holdings']:
            url = f"{DATA_API_HOST}/stocks/fundamental/v1/announcement?token={h}"
            headers = add_vensec_auth_to_headers(self.sessionid,self.clientid,self.auth)

            response = requests.request("GET", url, headers=headers, data={})
            tempres = response.json()

            if 'corporate_actions' not in res['user_portfolio']['holdings'][h]:
                res['user_portfolio']['holdings'][h]['corporate_actions'] = {}

            res['user_portfolio']['holdings'][h]['corporate_actions']['board_announcements'] = tempres



@corpActionRouter.get('/get_stock_corporate_actions')
@corpActionRouter.post('/get_stock_corporate_actions')
async def GetCorporateActions(request: Request, symbol: str):

    url = f"{DATA_API_HOST}/stocks/fundamental/v1/corpaction?token={master[symbol]}"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'),
                                         request.headers.get('Authorization'))

    response = requests.request("GET", url, headers=headers, data={})
    tempres = response.json()

    res = {'splits': tempres}
    return res


@corpActionRouter.get('/get_stock_dividends')
@corpActionRouter.post('/get_stock_dividends')
async def GetDividends(request: Request, symbol: str):
    url = f"{DATA_API_HOST}/stocks/fundamental/v1/dividend?token={master[symbol]}"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'),
                                         request.headers.get('Authorization'))

    response = requests.request("GET", url, headers=headers, data={})
    tempres = response.json()

    res = {}

    for t in tempres:
        t['dividend_percentage'] = t['perc']
        del t['perc']

    res['dividends'] = tempres

    return res

@corpActionRouter.get('/get_stock_board_announcements')
@corpActionRouter.post('/get_stock_board_announcements')
async def GetBoardAnnouncements(request: Request, symbol: str):
    url = f"{DATA_API_HOST}/stocks/fundamental/v1/announcement?token={master[symbol]}"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'),
                                         request.headers.get('Authorization'))

    response = requests.request("GET", url, headers=headers, data={})
    tempres = response.json()

    res = {'board_announcements': tempres}

    return res