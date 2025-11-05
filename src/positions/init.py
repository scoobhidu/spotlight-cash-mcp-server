import requests

from config import DATA_API_HOST
from headers_util import add_vensec_auth_to_headers
from fastapi import Request, APIRouter

positionsRouter = APIRouter()

class UserPositions:
    def __init__(self, clientid, sessionid, authorization):
        self.clientid = clientid
        self.sessionid = sessionid
        self.auth = authorization

    async def GetOpenPositions(request: Request):
        res = {}
        url = f"{DATA_API_HOST}/txn/positions/v3/summary"
        headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'),
                                             request.headers.get('Authorization'))
        payload = '{"client_id": "' + request.headers.get('x-client-id') + '"}'

        response = requests.request("POST", url, headers=headers, data=payload)

        restemp = response.json()

        res['total_profit_or_loss'] = restemp['result']['pl']
        res['realised_profit_or_loss'] = restemp['result']['rel_pl']
        res['unrealised_profit_or_loss'] = restemp['result']['unrel_pl']

        url = f"{DATA_API_HOST}/txn/positions/v4/list"
        headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'),
                                             request.headers.get('Authorization'))
        payload = '{"client_id": "' + request.headers.get(
            'x-client-id') + '", "sort_by": 1, "searchKey": "", "order_no": null}'

        response = requests.request("POST", url, headers=headers, data=payload)

        restemp = response.json()

        for pos in restemp['result']['positions']['opn_pos']:
            del pos['product_type']
            del pos['max_lmt_qty']
            del pos['inst_type']
            del pos['oc_token']
            del pos['is_mtf_enabled']
            pos['average_trade_price'] = pos['atp']
            del pos['atp']

        res['open_positions'] = restemp['result']['positions']['opn_pos']

        return res

@positionsRouter.get("/get_user_positions_summary")
@positionsRouter.post("/get_user_positions_summary")
async def GetOpenPositions(request: Request):
    res = {}
    url = f"{DATA_API_HOST}/txn/positions/v3/summary"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    payload = '{"client_id": "' + request.headers.get('x-client-id') + '"}'

    response = requests.request("POST", url, headers=headers, data=payload)

    restemp = response.json()

    res['total_profit_or_loss'] = restemp['result']['pl']
    res['realised_profit_or_loss'] = restemp['result']['rel_pl']
    res['unrealised_profit_or_loss'] = restemp['result']['unrel_pl']

    url = f"{DATA_API_HOST}/txn/positions/v4/list"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    payload = '{"client_id": "' + request.headers.get('x-client-id') + '", "sort_by": 1, "searchKey": "", "order_no": null}'

    response = requests.request("POST", url, headers=headers, data=payload)

    restemp = response.json()

    for pos in restemp['result']['positions']['opn_pos']:
        del pos['product_type']
        del pos['max_lmt_qty']
        del pos['inst_type']
        del pos['oc_token']
        del pos['is_mtf_enabled']
        pos['average_trade_price'] = pos['atp']
        del pos['atp']

    res['open_positions'] = restemp['result']['positions']['opn_pos']

    return res