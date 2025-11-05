import requests
from fastapi import Request, APIRouter

from config import DATA_API_HOST
from headers_util import add_vensec_auth_to_headers

globalRouter = APIRouter()

class GlobalIndices:
    def __init__(self, clientid, sessionid, authorization):
        self.clientid = clientid
        self.sessionid = sessionid
        self.auth = authorization

    async def get_global_cues(self, res):
        url = f"{DATA_API_HOST}/indices/v1/global"
        headers = add_vensec_auth_to_headers(self.sessionid, self.clientid, self.auth)

        response = requests.request("GET", url, headers=headers, data={})

        tempres = response.json()

        res['global_market_cues'] = {}
        for market in tempres['data']:
            res['global_market_cues'][market['name']] = {}
            res['global_market_cues'][market['name']]['ltp'] = market['c']
            res['global_market_cues'][market['name']]['absolute_change_in_market_session'] = market['diff']
            res['global_market_cues'][market['name']]['percentage_change_in_market_session'] = market['nci']
            res['global_market_cues'][market['name']]['country'] = market['country']
            res['global_market_cues'][market['name']]['live'] = market['live']


@globalRouter.get("/global_indices_movement")
@globalRouter.post("/global_indices_movement")
async def get_global_cues(request: Request):
    url = f"{DATA_API_HOST}/indices/v1/global"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    res = {}
    res['global_market_cues'] = {}

    for market in tempres['data']:
        res['global_market_cues'][market['name']] = {}
        res['global_market_cues'][market['name']]['ltp'] = market['c']
        res['global_market_cues'][market['name']]['absolute_change_in_market_session'] = market['diff']
        res['global_market_cues'][market['name']]['percentage_change_in_market_session'] = market['nci']
        res['global_market_cues'][market['name']]['country'] = market['country']
        res['global_market_cues'][market['name']]['live'] = market['live']

    return res
