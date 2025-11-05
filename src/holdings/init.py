import requests

from config import DATA_API_HOST
from headers_util import add_vensec_auth_to_headers
from fastapi import Request, APIRouter

holdingRouter = APIRouter()

class UserHoldings:
    def __init__(self, clientid, sessionid, authorization):
        self.clientid = clientid
        self.sessionid = sessionid
        self.auth = authorization

    async def GetHoldings(self, futlist):
        url = f"{DATA_API_HOST}/txn/holding/v4/get"
        headers = add_vensec_auth_to_headers(self.sessionid,self.clientid,self.auth)
        payload = '{"sort_by": 1}'

        response = requests.request("POST", url, headers=headers, data=payload)

        res = {}
        restemp = response.json()

        res['portfolio_current_market_value'] = restemp[0]
        res['portfolio_invested_value'] = restemp[1]
        res['portfolio_days_pnl_absolute'] = restemp[2]
        res['portfolio_days_pnl_percentage_change'] = restemp[3]
        res['portfolio_total_pnl_absolute'] = restemp[4]
        res['portfolio_total_pnl_percentage_change'] = restemp[5]
        res['total_stocks'] = restemp[6]

        res['holdings'] = {}

        for holding in restemp[8]:
            res['holdings'][holding[3]] = {}
            res['holdings'][holding[3]]['sym'] = holding[0]
            res['holdings'][holding[3]]['exch'] = holding[1]
            res['holdings'][holding[3]]['nse_token'] = holding[3]
            res['holdings'][holding[3]]['bse_token'] = holding[4]
            res['holdings'][holding[3]]['invested_amount'] = holding[5]
            res['holdings'][holding[3]]['total_qty'] = holding[6]
            res['holdings'][holding[3]]['ltp'] = holding[7]
            res['holdings'][holding[3]]['current_market_value'] = holding[8]
            res['holdings'][holding[3]]['pledged_qty'] = holding[11]
            res['holdings'][holding[3]]['average_bought_price'] = holding[12]
            res['holdings'][holding[3]]['days_pnl_absolute'] = holding[14]
            res['holdings'][holding[3]]['days_pnl_percentage_change'] = holding[15]
            res['holdings'][holding[3]]['overall_pnl_absolute'] = holding[16]
            res['holdings'][holding[3]]['overall_pnl_percentage_change'] = holding[17]
            res['holdings'][holding[3]]['company_name'] = holding[19]

            if res['holdings'][holding[3]]['sym'] in futlist:
                res['holdings'][holding[3]]['has_future_contract'] = True
                res['holdings'][holding[3]]['future_contract_lot_size'] = futlist[res['holdings'][holding[3]]['sym']]['lot_size']
                res['holdings'][holding[3]]['max_pain'] = futlist[res['holdings'][holding[3]]['sym']]['max_pain']
            else:
                res['holdings'][holding[3]]['has_future_contract'] = False

        return res



@holdingRouter.get("/get_user_portfolio")
@holdingRouter.post("/get_user_portfolio")
async def GetHoldings(request: Request):
    url = f"{DATA_API_HOST}/txn/holding/v4/get"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    payload = '{"sort_by": 1}'

    response = requests.request("POST", url, headers=headers, data=payload)

    res = {}
    restemp = response.json()

    res['portfolio_current_market_value'] = restemp[0]
    res['portfolio_invested_value'] = restemp[1]
    res['portfolio_days_pnl_absolute'] = restemp[2]
    res['portfolio_days_pnl_percentage_change'] = restemp[3]
    res['portfolio_total_pnl_absolute'] = restemp[4]
    res['portfolio_total_pnl_percentage_change'] = restemp[5]
    res['total_stocks'] = restemp[6]

    res['holdings'] = {}

    for holding in restemp[8]:
        res['holdings'][holding[3]] = {}
        res['holdings'][holding[3]]['sym'] = holding[0]
        res['holdings'][holding[3]]['exch'] = holding[1]
        res['holdings'][holding[3]]['nse_token'] = holding[3]
        res['holdings'][holding[3]]['bse_token'] = holding[4]
        res['holdings'][holding[3]]['invested_amount'] = holding[5]
        res['holdings'][holding[3]]['total_qty'] = holding[6]
        res['holdings'][holding[3]]['ltp'] = holding[7]
        res['holdings'][holding[3]]['current_market_value'] = holding[8]
        res['holdings'][holding[3]]['pledged_qty'] = holding[11]
        res['holdings'][holding[3]]['average_bought_price'] = holding[12]
        res['holdings'][holding[3]]['days_pnl_absolute'] = holding[14]
        res['holdings'][holding[3]]['days_pnl_percentage_change'] = holding[15]
        res['holdings'][holding[3]]['overall_pnl_absolute'] = holding[16]
        res['holdings'][holding[3]]['overall_pnl_percentage_change'] = holding[17]
        res['holdings'][holding[3]]['company_name'] = holding[19]

    return res