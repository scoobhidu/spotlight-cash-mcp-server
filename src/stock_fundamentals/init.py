import requests
from fastapi import APIRouter, Request

from config import master, DATA_API_HOST
from headers_util import add_niftytrader_auth_to_headers, add_vensec_auth_to_headers

fundaRouter = APIRouter()

class StockFundamentals:
    def __init__(self, clientid, sessionid, authorization):
        self.clientid = clientid
        self.sessionid = sessionid
        self.auth = authorization

    async def GetFundamentalSummary(self, res):
        for h in res['user_portfolio']['holdings']:
            url = f"{DATA_API_HOST}/stocks/fundamental/v1/complete?token={h}"
            headers = add_vensec_auth_to_headers(self.sessionid,self.clientid,self.auth)

            response = requests.request("GET", url, headers=headers, data={})

            tempres = response.json()

            tempres['shareholding']['foreign_investors'] = tempres['shareholding']['fi']
            tempres['shareholding']['foreign_institutional_investors'] = tempres['shareholding']['fii']
            tempres['shareholding']['mutual_funds'] = tempres['shareholding']['mf']

            del tempres['shareholding']['fi']
            del tempres['shareholding']['fii']
            del tempres['shareholding']['mf']

            res['user_portfolio']['holdings'][h]['shareholding_pattern'] = tempres['shareholding']
            res['user_portfolio']['holdings'][h]['industry'] = tempres['overview']['industry']
            res['user_portfolio']['holdings'][h]['about_company'] = tempres['overview']['about']

            res['user_portfolio']['holdings'][h]['promoter_holding_pattern'] = []

            for i in range(len(tempres['promoterholding']['date'])):
                res['user_portfolio']['holdings'][h]['promoter_holding_pattern'].append({
                    'date': tempres['promoterholding']['date'][i],
                    'holding_percentage': tempres['promoterholding']['holding'][i],
                    'pledged_percentage': tempres['promoterholding']['pledge'][i],
                })


@fundaRouter.get('/get_stock_fundamental_data')
@fundaRouter.post('/get_stock_fundamental_data')
async def GetFundamentalSummary(request: Request, symbol: str):
    url = f"{DATA_API_HOST}/stocks/fundamental/v1/complete?token={master[symbol]}"
    headers = add_vensec_auth_to_headers(client_id=request.headers.get('x-client-id'), session_id=request.headers.get('session_id'), auth=request.headers.get("Authorization"))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()
    if 'shareholding' in tempres:
        tempres['shareholding']['foreign_investors'] = tempres['shareholding']['fi']
        tempres['shareholding']['foreign_institutional_investors'] = tempres['shareholding']['fii']
        tempres['shareholding']['mutual_funds'] = tempres['shareholding']['mf']

        del tempres['shareholding']['fi']
        del tempres['shareholding']['fii']
        del tempres['shareholding']['mf']
    else:
        tempres['shareholding'] = 'shareholding data not available'

    res = {}
    if 'overview' in tempres:
        res['industry'] = tempres['overview']['industry']
        res['about_company'] = tempres['overview']['about']

    res['shareholding_pattern'] = tempres['shareholding'],
    res['promoter_holding_pattern']: []

    for i in range(len(tempres['promoterholding']['date'])):
        if 'promoter_holding_pattern' not in res:
            res['promoter_holding_pattern'] = []

        res['promoter_holding_pattern'].append({
            'date': tempres['promoterholding']['date'][i],
            'holding_percentage': tempres['promoterholding']['holding'][i],
            'pledged_percentage': tempres['promoterholding']['pledge'][i],
        })

    return res
