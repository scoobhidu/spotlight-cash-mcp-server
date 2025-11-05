import requests
from fastapi import APIRouter, Request

from config import DATA_API_HOST
from headers_util import add_vensec_auth_to_headers

indianSectorRouter = APIRouter()

class IndianSectorBreakup:
    def __init__(self, clientid, sessionid, authorization):
        self.clientid = clientid
        self.sessionid = sessionid
        self.auth = authorization

    async def get_indian_sector_movement(self, res):
        url = f"{DATA_API_HOST}/stocks/trends/v1/sectormovement"
        headers = add_vensec_auth_to_headers(self.sessionid, self.clientid, self.auth)

        response = requests.request("GET", url, headers=headers, data={})

        tempres = response.json()

        res['indian_sector_movement_analysis'] = {}
        for sector in tempres:
            res['indian_sector_movement_analysis'][sector['sector']] = {
                'advance': sector['adv'],
                'decline': sector['dec'],
                'neutral': sector['neutral'],
            }


@indianSectorRouter.get('/indian_sector_movement')
@indianSectorRouter.post('/indian_sector_movement')
async def get_indian_sector_movement(request: Request):
    url = f"{DATA_API_HOST}/stocks/trends/v1/sectormovement"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    res = {'indian_sector_movement_analysis': {}}
    for sector in tempres:
        res['indian_sector_movement_analysis'][sector['sector']] = {
            'advance': sector['adv'],
            'decline': sector['dec'],
            'neutral': sector['neutral'],
        }

    return res


