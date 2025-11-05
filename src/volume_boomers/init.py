import requests
from fastapi import APIRouter, Request

from config import DATA_API_HOST
from headers_util import add_vensec_auth_to_headers

volumeRouter = APIRouter()

class VolumeBoomers:
    def __init__(self, clientid, sessionid, authorization):
        self.clientid = clientid
        self.sessionid = sessionid
        self.auth = authorization

    async def get_volume_boomer_stocks(self, res):
        url = f"{DATA_API_HOST}/stocks/watchlist/v4/watchlist/view?client_id={self.clientid}&wl_id=3691"
        headers = add_vensec_auth_to_headers(self.sessionid, self.clientid, self.auth)

        response = requests.request("GET", url, headers=headers, data={})

        tempres = response.json()
        for boomer in tempres['result']:
            if boomer['nse_token'] in res['user_portfolio']['holdings']:
                res['user_portfolio']['holdings'][boomer['nse_token']]['volume_boomer_in_24_hours'] = True
                res['user_portfolio']['holdings'][boomer['nse_token']]['volume_percentage_change_in_24_hours'] = boomer['vol_nci']
                res['user_portfolio']['holdings'][boomer['nse_token']]['volume_change_in_24_hrs'] = boomer['vol']


@volumeRouter.get('/get_stock_volume_boomers')
@volumeRouter.post('/get_stock_volume_boomers')
async def get_volume_boomer_stocks(request: Request):
    url = f"https://{DATA_API_HOST}/stocks/watchlist/v4/watchlist/view?client_id={request.headers.get('x-client-id')}&wl_id=3691"
    headers = add_vensec_auth_to_headers(client_id=request.headers.get('x-client-id'),
                                         session_id=request.headers.get('session_id'),
                                         auth=request.headers.get("Authorization"))


    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    for boomer in tempres['result']:
        del boomer['bse_token']
        del boomer['nse_token']
        del boomer['exch']
        del boomer['mchart']
        del boomer['pclose']
        del boomer['type']

        boomer['ltp_percentage_change'] = boomer['nci']
        del boomer['nci']

    return tempres