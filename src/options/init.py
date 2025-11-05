import requests
from fastapi import APIRouter, Request

from headers_util import add_niftytrader_auth_to_headers


pcrRouter = APIRouter()

class StockOptions:
    def __init__(self, niftytraderauth):
        self.niftytraderauth = niftytraderauth

    async def GetOIPcrData(self, res):
        for h in res['user_portfolio']['holdings']:
            if res['user_portfolio']['holdings'][h]['has_future_contract']:
                url = f"https://services.niftytrader.in/webapi/option/oi-pcr-data?type=otherpcr&expiry=&symbol={res['user_portfolio']['holdings'][h]['sym']}"
                headers = add_niftytrader_auth_to_headers(self.niftytraderauth)

                response = requests.request("GET", url, headers=headers, data={})

                tempres = response.json()
                res['user_portfolio']['holdings'][h]['oi_pcr_data'] = {}
                res['user_portfolio']['holdings'][h]['oi_pcr_data']['expiry_date'] = tempres['result']['oiDatas'][0]['expiry_date']

                chartData= []
                for oi in tempres['result']['oiDatas']:
                    chartData.append({
                        'oi_pcr_data': oi['pcr'],
                        'stock_value': oi['index_close'],
                        'time': oi['time'],
                    })
                res['user_portfolio']['holdings'][h]['oi_pcr_data']['oi_pcr'] = chartData

            return None
        return None

    async def GetFutureOITimeseries(self, res):
        for h in res['user_portfolio']['holdings']:
            if res['user_portfolio']['holdings'][h]['has_future_contract']:
                url = f"https://webapi.niftytrader.in/webapi/Symbol/future-expiry-chart-data?symbol={res['user_portfolio']['holdings'][h]['sym']}&interval=day20"
                headers = add_niftytrader_auth_to_headers(self.niftytraderauth)

                response = requests.request("GET", url, headers=headers, data={})

                tempres = response.json()

                tempres['fut_oi_day_trend'] = []
                if 'chart_data' in tempres:
                    tempres['chart_data'] = tempres['chart_data'].split(',')
                    tempres['created_at'] = tempres['created_at'].split(',')

                    for i in range(len(tempres['chart_data'])):
                        tempres['fut_oi_day_trend'].append({
                            'oi': tempres['chart_data'][i],
                            'time': tempres['created_at'][i],
                        })

                    del tempres['chart_data']
                    del tempres['created_at']

                res['user_portfolio']['holdings'][h]['fut_oi'] = tempres['fut_oi_day_trend']
            return None
        return None


@pcrRouter.get("/get_oi_pcr_data")
@pcrRouter.post("/get_oi_pcr_data")
async def GetOIPcrData(request: Request, symbol: str):
    url = f"https://services.niftytrader.in/webapi/option/oi-pcr-data?type=otherpcr&expiry=&symbol={symbol}"
    headers = add_niftytrader_auth_to_headers(request.headers.get('niftytraderauth'))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    res = {'oi_pcr_data': {}}
    res['oi_pcr_data']['expiry_date'] = tempres['result']['oiDatas'][0]['expiry_date']

    chartData= []
    for oi in tempres['result']['oiDatas']:
        chartData.append({
            'oi_pcr_data': oi['pcr'],
            'stock_value': oi['index_close'],
            'time': oi['time'],
        })
    res['oi_pcr_data']['oi_pcr'] = chartData

    return res

@pcrRouter.get("/get_fut_oi_timeseries_data")
@pcrRouter.post("/get_fut_oi_timeseries_data")
async def GetFutureOITimeseries(request: Request, symbol: str):
    url = f"https://webapi.niftytrader.in/webapi/Symbol/future-expiry-chart-data?symbol={symbol}&interval=day20"
    headers = add_niftytrader_auth_to_headers(request.headers.get('niftytraderauth'))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    res = {}
    if 'resultData' in tempres:
        for expiries in tempres['resultData']:
            expiries['fut_oi_day_trend'] = []

            expiries['chart_data'] = expiries['chart_data'].split(',')
            expiries['created_at'] = expiries['created_at'].split(',')

            for i in range(len(expiries['chart_data'])):
                expiries['fut_oi_day_trend'].append({
                    'oi': expiries['chart_data'][i],
                    'time': expiries['created_at'][i],
                })

            del expiries['chart_data']
            del expiries['created_at']

    res['fut_oi'] = tempres['resultData']

    return res