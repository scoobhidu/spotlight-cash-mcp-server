from os.path import split

import requests
from fastapi import Request, APIRouter

from config import DATA_API_HOST
from headers_util import add_niftytrader_auth_to_headers, add_vensec_auth_to_headers

indianRouter = APIRouter()

class IndianIndices:
    def __init__(self, clientid, sessionid, authorization, niftytraderauth):
        self.clientid = clientid
        self.sessionid = sessionid
        self.auth = authorization

        self.niftytraderauth = niftytraderauth

    async def GetMajorIndianIndicesData(self, res):
        url = f"https://webapi.niftytrader.in/webapi/symbol/stock-index-data"
        headers = add_niftytrader_auth_to_headers(self.niftytraderauth)

        response = requests.request("GET", url, headers=headers, data={})

        return response.json()

    async def GetVixData(self, res):
        url = f"https://services.niftytrader.in/webapi/symbol/other-symbol-spot-data?symbol=INDIA+VIX"
        headers = add_niftytrader_auth_to_headers(self.niftytraderauth)

        response = requests.request("GET", url, headers=headers, data={})

        tempres =  response.json()

        res['india_vix_data'] = {}
        res['india_vix_data']['open'] = tempres['result']['open']
        res['india_vix_data']['high'] = tempres['result']['high']
        res['india_vix_data']['low'] = tempres['result']['low']
        res['india_vix_data']['close'] = tempres['result']['close']
        res['india_vix_data']['absolute_change_in_session'] = tempres['result']['change']

        chartData = (tempres['result']['chart_data']).split(',')
        chartTime = (tempres['result']['chart_time']).split(',')
        res['india_vix_data']['5_min_timeseries_data_during_session'] = []
        for i in range(len(chartData)):
            res['india_vix_data']['5_min_timeseries_data_during_session'].append({
                'time': chartTime[i],
                'value': chartData[i],
            })


    async def GetSectoralIndices(self):
        url = f"{DATA_API_HOST}/indices/v1/summary"
        headers = add_vensec_auth_to_headers(client_id=self.clientid, session_id=self.sessionid, auth=self.auth)

        response = requests.request("GET", url, headers=headers, data={})

        return response.json()

    async def GetAllIndianIndices(self):
        url = f"{DATA_API_HOST}/indices/v1/viewall"
        headers = add_vensec_auth_to_headers(client_id=self.clientid, session_id=self.sessionid, auth=self.auth)

        response = requests.request("GET", url, headers=headers, data={})

        return response.json()



@indianRouter.get("/get_major_indian_indices_movement")
@indianRouter.post("/get_major_indian_indices_movement")
async def GetMajorIndianIndicesData(request: Request):
    url = f"https://webapi.niftytrader.in/webapi/symbol/stock-index-data"
    headers = add_niftytrader_auth_to_headers(request.headers.get('niftytraderauth'))

    response = requests.request("GET", url, headers=headers, data={})

    return response.json()


@indianRouter.get("/india_vix_movement")
@indianRouter.post("/india_vix_movement")
async def GetVixData(request: Request):
    url = f"https://services.niftytrader.in/webapi/symbol/other-symbol-spot-data?symbol=INDIA+VIX"
    headers = add_niftytrader_auth_to_headers(request.headers.get('niftytraderauth'))

    response = requests.request("GET", url, headers=headers, data={})

    tempres =  response.json()
    res = {}
    res['india_vix_data'] = {}
    res['india_vix_data']['open'] = tempres['result']['open']
    res['india_vix_data']['high'] = tempres['result']['high']
    res['india_vix_data']['low'] = tempres['result']['low']
    res['india_vix_data']['close'] = tempres['result']['close']
    res['india_vix_data']['absolute_change_in_session'] = tempres['result']['change']

    chartData = (tempres['result']['chart_data']).split(',')
    chartTime = (tempres['result']['chart_time']).split(',')
    res['india_vix_data']['5_min_timeseries_data_during_session'] = []
    for i in range(len(chartData)):
        res['india_vix_data']['5_min_timeseries_data_during_session'].append({
            'time': chartTime[i],
            'value': chartData[i],
        })

    return res


@indianRouter.get("/indian_indices_movement")
@indianRouter.post("/indian_indices_movement")
async def GetSectoralIndices(request: Request):
    url = f"{DATA_API_HOST}/indices/v1/summary"
    headers = add_vensec_auth_to_headers(client_id=request.headers.get('x-client-id'), session_id=request.headers.get('session_id'), auth=request.headers.get("Authorization"))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    for index in tempres['Benchmark Indices']:
        del index['order_by']

    return tempres

