import requests
from fastapi import APIRouter, Request

from config import DATA_API_HOST
from headers_util import add_vensec_auth_to_headers

indexChartRouter = APIRouter()

@indexChartRouter.get('/index_line_chart')
@indexChartRouter.post('/index_line_chart')
async def get_nfo_line_chart(request: Request, symbol: str, period: str):
    sym = symbol.replace(" ", "%20")
    url = f"{DATA_API_HOST}/indices/v1/linechart?token={sym}&period={period}"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    return tempres