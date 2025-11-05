import requests
from fastapi import APIRouter, Request

from config import DATA_API_HOST
from headers_util import add_vensec_auth_to_headers


portfolioAnalyticsRouter = APIRouter()

class PortfolioAnalytics:
    def __init__(self, clientid, sessionid, authorization):
        self.clientid = clientid
        self.sessionid = sessionid
        self.auth = authorization

    async def get_holding_ltq_stq(self, res):
        url = f"{DATA_API_HOST}/portfolio-analytics/holdingdetails"
        headers = add_vensec_auth_to_headers(self.sessionid, self.clientid, self.auth)

        response = requests.request("GET", url, headers=headers, data={})

        tempres = response.json()

        del tempres['externalApiFailed']
        for holding in tempres['result']:
            for h in res['user_portfolio']['holdings']:
                if res['user_portfolio']['holdings'][h]['sym'] == holding['symbol']:
                    res['user_portfolio']['holdings'][h]['short_term_holding_quantity'] = holding['stQty']
                    res['user_portfolio']['holdings'][h]['long_term_holding_quantity'] = holding['ltQty']


    async def get_holding_mcap_allocation_sector(self, res):
        url = f"{DATA_API_HOST}/portfolio-analytics/marketcap?isSectorView=true"
        headers = add_vensec_auth_to_headers(self.sessionid, self.clientid, self.auth)

        response = requests.request("GET", url, headers=headers, data={})

        return response.json()

@portfolioAnalyticsRouter.get('/get_holding_ltq_stq')
@portfolioAnalyticsRouter.post('/get_holding_ltq_stq')
async def get_holding_ltq_stq(request: Request):
    url = f"{DATA_API_HOST}/portfolio-analytics/holdingdetails"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    del tempres['externalApiFailed']

    return tempres


@portfolioAnalyticsRouter.get('/get_holding_mcaps_allocations_sectors')
@portfolioAnalyticsRouter.post('/get_holding_mcaps_allocations_sectors')
async def get_holding_mcap_allocation_sector(request: Request):
    url = f"{DATA_API_HOST}/portfolio-analytics/marketcap?isSectorView=true"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    response = requests.request("GET", url, headers=headers, data={})

    return response.json()
