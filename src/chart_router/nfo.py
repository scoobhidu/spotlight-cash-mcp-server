import requests
from fastapi import APIRouter, Request

from config import master, DATA_API_HOST
from headers_util import add_vensec_auth_to_headers

nfoChartRouter = APIRouter()

@nfoChartRouter.get('/nfo_line_chart')
@nfoChartRouter.post('/nfo_line_chart')
async def get_nfo_line_chart(request: Request, symbol: str, period: str):
    url = f"{DATA_API_HOST}/fno/v2/linechart?token={master[symbol]}&period={period}"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    return tempres