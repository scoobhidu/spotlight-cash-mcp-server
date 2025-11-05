from fastapi import APIRouter, Request
import requests

from config import DATA_API_HOST
from headers_util import add_vensec_auth_to_headers

trendsRouter = APIRouter()


@trendsRouter.get('/52w_high')
@trendsRouter.post('/52w_high')
async def get_gainers(request: Request):
    # Default query params
    period = "52w"
    page = request.query_params.get("page", "0")
    size = request.query_params.get("size", "10")

    url = f"{DATA_API_HOST}/stocks/nse/trends/v2/high?period={period}&page={page}&size={size}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    response = requests.get(url, headers=headers)
    tempres = response.json()

    del tempres['total']
    del tempres['size']
    for stocks in tempres['data']:
        del stocks['mchart']
        del stocks['is_mtf_enabled']
        del stocks['is_wl']

        stocks['optionchain_spot_token'] = stocks['oc_token']
        del stocks['oc_token']

        stocks['user_holding_qty'] = stocks['h_qty']
        del stocks['h_qty']

    return tempres

@trendsRouter.get('/1d_high')
@trendsRouter.post('/1d_high')
async def get_gainers(request: Request):
    # Default query params
    period = "1d"
    page = request.query_params.get("page", "0")
    size = request.query_params.get("size", "15")

    url = f"{DATA_API_HOST}/stocks/nse/trends/v2/high?period={period}&page={page}&size={size}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    response = requests.get(url, headers=headers)
    tempres = response.json()

    del tempres['total']
    del tempres['size']
    for stocks in tempres['data']:
        del stocks['mchart']
        del stocks['is_mtf_enabled']
        del stocks['is_wl']

        stocks['optionchain_spot_token'] = stocks['oc_token']
        del stocks['oc_token']

        stocks['user_holding_qty'] = stocks['h_qty']
        del stocks['h_qty']

    return tempres


@trendsRouter.get('/52w_low')
@trendsRouter.post('/52w_low')
async def get_gainers(request: Request):
    # Default query params
    period = "52w"
    page = request.query_params.get("page", "0")
    size = request.query_params.get("size", "15")

    url = f"{DATA_API_HOST}/stocks/nse/trends/v2/low?period={period}&page={page}&size={size}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    response = requests.get(url, headers=headers)
    tempres = response.json()

    del tempres['total']
    del tempres['size']
    for stocks in tempres['data']:
        del stocks['mchart']
        del stocks['is_mtf_enabled']
        del stocks['is_wl']

        stocks['optionchain_spot_token'] = stocks['oc_token']
        del stocks['oc_token']

        stocks['user_holding_qty'] = stocks['h_qty']
        del stocks['h_qty']

    return tempres


@trendsRouter.get('/1d_low')
@trendsRouter.post('/1d_low')
async def get_gainers(request: Request):
    # Default query params
    period = "1d"
    page = request.query_params.get("page", "0")
    size = request.query_params.get("size", "15")

    url = f"{DATA_API_HOST}/stocks/nse/trends/v2/low?period={period}&page={page}&size={size}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    response = requests.get(url, headers=headers)
    tempres = response.json()

    del tempres['total']
    del tempres['size']
    for stocks in tempres['data']:
        del stocks['mchart']
        del stocks['is_mtf_enabled']
        del stocks['is_wl']

        stocks['optionchain_spot_token'] = stocks['oc_token']
        del stocks['oc_token']

        stocks['user_holding_qty'] = stocks['h_qty']
        del stocks['h_qty']

    return tempres


@trendsRouter.get('/gainers')
@trendsRouter.post('/gainers')
async def get_gainers(request: Request):
    # Default query params
    period = request.query_params.get("period", "1d")
    page = request.query_params.get("page", "0")
    size = request.query_params.get("size", "15")

    url = f"{DATA_API_HOST}/stocks/trends/v2/gainers?period={period}&page={page}&size={size}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    response = requests.get(url, headers=headers)
    tempres = response.json()

    del tempres['size']
    for stocks in tempres['data']:
        del stocks['mchart']
        del stocks['is_mtf_enabled']

        stocks['optionchain_spot_token'] = stocks['oc_token']
        del stocks['oc_token']

    return tempres

@trendsRouter.get('/losers')
@trendsRouter.post('/losers')
async def get_gainers(request: Request):
    # Default query params
    period = request.query_params.get("period", "1d")
    page = request.query_params.get("page", "0")
    size = request.query_params.get("size", "15")

    url = f"{DATA_API_HOST}/stocks/trends/v2/losers?period={period}&page={page}&size={size}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    response = requests.get(url, headers=headers)
    tempres = response.json()

    del tempres['size']
    for stocks in tempres['data']:
        del stocks['mchart']
        del stocks['is_mtf_enabled']

        stocks['optionchain_spot_token'] = stocks['oc_token']
        del stocks['oc_token']

    return tempres


#### NIFTY 100 sort by volume today
@trendsRouter.get('/byvolume')
@trendsRouter.post('/byvolume')
async def get_by_volume(request: Request):
    # Default query params
    page = request.query_params.get("page", "0")
    size = request.query_params.get("size", "15")

    url = f"{DATA_API_HOST}/stocks/trends/v2/byvolume?page={page}&size={size}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    response = requests.get(url, headers=headers)
    tempres = response.json()

    del tempres['total']
    del tempres['size']
    for stocks in tempres['data']:
        del stocks['mchart']
        del stocks['is_mtf_enabled']
        del stocks['is_wl']

        stocks['optionchain_spot_token'] = stocks['oc_token']
        del stocks['oc_token']

        stocks['user_holding_qty'] = stocks['h_qty']
        del stocks['h_qty']

        stocks['volume'] = stocks['vol']
        del stocks['vol']

    return tempres


#### NIFTY 100 sort by ltp * volume today
@trendsRouter.get('/byvalue')
@trendsRouter.post('/byvalue')
async def get_by_volume(request: Request):
    # Default query params
    page = request.query_params.get("page", "0")
    size = request.query_params.get("size", "15")

    url = f"{DATA_API_HOST}/stocks/trends/v2/byvalue?page={page}&size={size}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    response = requests.get(url, headers=headers)
    tempres = response.json()

    del tempres['total']
    del tempres['size']
    for stocks in tempres['data']:
        del stocks['mchart']
        del stocks['is_mtf_enabled']
        del stocks['is_wl']

        stocks['optionchain_spot_token'] = stocks['oc_token']
        del stocks['oc_token']

        stocks['user_holding_qty'] = stocks['h_qty']
        del stocks['h_qty']

        stocks['value'] = stocks['val']
        del stocks['val']

    return tempres


@trendsRouter.get('/curated/peratio')
@trendsRouter.post('/curated/peratio')
async def get_curated_pe_ratio(request: Request):
    # Query params
    page = request.query_params.get("page", "0")
    size = request.query_params.get("size", "50")

    url = f"{DATA_API_HOST}/market/v2/curated/peratio?page={page}&size={size}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    response = requests.get(url, headers=headers)
    tempres = response.json()

    del tempres['total']
    del tempres['size']
    for stocks in tempres['lists']:
        del stocks['mchart']
        del stocks['is_mtf_enabled']
        del stocks['is_wl']

        stocks['optionchain_spot_token'] = stocks['oc_token']
        del stocks['oc_token']

        stocks['user_holding_qty'] = stocks['h_qty']
        del stocks['h_qty']

        stocks['price_to_earning_ratio'] = stocks['pe']
        del stocks['pe']

    return tempres


@trendsRouter.get('/curated/roe')
@trendsRouter.post('/curated/roe')
async def get_curated_pe_ratio(request: Request):
    # Query params
    page = request.query_params.get("page", "0")
    size = request.query_params.get("size", "50")

    url = f"{DATA_API_HOST}/market/v2/curated/roe?page={page}&size={size}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    response = requests.get(url, headers=headers)
    tempres = response.json()

    del tempres['total']
    del tempres['size']
    for stocks in tempres['lists']:
        del stocks['mchart']
        del stocks['is_mtf_enabled']
        del stocks['is_wl']

        stocks['optionchain_spot_token'] = stocks['oc_token']
        del stocks['oc_token']

        stocks['user_holding_qty'] = stocks['h_qty']
        del stocks['h_qty']

        stocks['return_on_earning_ratio'] = stocks['roe']
        del stocks['roe']

    return tempres


@trendsRouter.get('/curated/dividend')
@trendsRouter.post('/curated/dividend')
async def get_curated_pe_ratio(request: Request):
    # Query params
    page = request.query_params.get("page", "0")
    size = request.query_params.get("size", "50")

    url = f"{DATA_API_HOST}/market/v2/curated/divpaying?page={page}&size={size}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    response = requests.get(url, headers=headers)
    tempres = response.json()

    del tempres['total']
    del tempres['size']
    for stocks in tempres['lists']:
        del stocks['mchart']
        del stocks['is_mtf_enabled']
        del stocks['is_wl']

        stocks['optionchain_spot_token'] = stocks['oc_token']
        del stocks['oc_token']

        stocks['user_holding_qty'] = stocks['h_qty']
        del stocks['h_qty']

        stocks['dividend_yield'] = stocks['div_yield']
        del stocks['div_yield']

    return tempres


@trendsRouter.get('/curated/roce')
@trendsRouter.post('/curated/roce')
async def get_curated_pe_ratio(request: Request):
    # Query params
    page = request.query_params.get("page", "0")
    size = request.query_params.get("size", "50")

    url = f"{DATA_API_HOST}/market/v2/curated/roce?page={page}&size={size}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    response = requests.get(url, headers=headers)
    tempres = response.json()

    del tempres['total']
    del tempres['size']
    for stocks in tempres['lists']:
        del stocks['mchart']
        del stocks['is_mtf_enabled']
        del stocks['is_wl']

        stocks['optionchain_spot_token'] = stocks['oc_token']
        del stocks['oc_token']

        stocks['user_holding_qty'] = stocks['h_qty']
        del stocks['h_qty']

        stocks['return_on_capital_employed'] = stocks['roce']
        del stocks['roce']

    return tempres


@trendsRouter.get('/curated/zerodebt')
@trendsRouter.post('/curated/zerodebt')
async def get_curated_pe_ratio(request: Request):
    # Query params
    page = request.query_params.get("page", "0")
    size = request.query_params.get("size", "50")

    url = f"{DATA_API_HOST}/market/v2/curated/zerodebt?page={page}&size={size}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    response = requests.get(url, headers=headers)
    tempres = response.json()

    del tempres['total']
    del tempres['size']
    for stocks in tempres['lists']:
        del stocks['mchart']
        del stocks['is_mtf_enabled']
        del stocks['is_wl']

        stocks['optionchain_spot_token'] = stocks['oc_token']
        del stocks['oc_token']

        stocks['user_holding_qty'] = stocks['h_qty']
        del stocks['h_qty']

    return tempres


@trendsRouter.get('/curated/ronw')
@trendsRouter.post('/curated/ronw')
async def get_curated_pe_ratio(request: Request):
    # Query params
    page = request.query_params.get("page", "0")
    size = request.query_params.get("size", "50")

    url = f"{DATA_API_HOST}/market/v2/curated/ronw?page={page}&size={size}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    response = requests.get(url, headers=headers)
    tempres = response.json()

    del tempres['total']
    del tempres['size']
    for stocks in tempres['lists']:
        del stocks['mchart']
        del stocks['is_mtf_enabled']
        del stocks['is_wl']

        stocks['optionchain_spot_token'] = stocks['oc_token']
        del stocks['oc_token']

        stocks['user_holding_qty'] = stocks['h_qty']
        del stocks['h_qty']

        stocks['return_on_assets'] = stocks['roa']
        del stocks['roa']

    return tempres


@trendsRouter.get('/curated/eps')
@trendsRouter.post('/curated/eps')
async def get_curated_pe_ratio(request: Request):
    # Query params
    page = request.query_params.get("page", "0")
    size = request.query_params.get("size", "50")

    url = f"{DATA_API_HOST}/market/v2/curated/eps?page={page}&size={size}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    response = requests.get(url, headers=headers)
    tempres = response.json()

    del tempres['total']
    del tempres['size']
    for stocks in tempres['lists']:
        del stocks['mchart']
        del stocks['is_mtf_enabled']
        del stocks['is_wl']

        stocks['optionchain_spot_token'] = stocks['oc_token']
        del stocks['oc_token']

        stocks['user_holding_qty'] = stocks['h_qty']
        del stocks['h_qty']

        stocks['earning_per_share'] = stocks['eps']
        del stocks['eps']

    return tempres


@trendsRouter.get('/filter/stocks/nse')
@trendsRouter.post('/filter/stocks/nse')
async def filter_stocks_nse(request: Request):
    url = f"{DATA_API_HOST}/filter/v2/stocks/nse"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    # Take JSON body from client request
    body = await request.json()
    payload = {
        "page": body['page'],
        "size": 5,
        "indices": body['indices'],
        "subsector": body['subsector'],
        "mcap_range": body['mcap_range'],
        "pe_range": body['pe_range'],
        "sortby": "DESC",
        "filterby": "mcap",
        "searchkey": body['searchkey']
    }
    response = requests.post(url, headers=headers, json=payload)
    tempres = response.json()

    for stock in tempres['result']:
        stock['mcap'] = f"{stock['market_cap']} Crores"
        del stock['market_cap']
        del stock['base_url']
        del stock['is_mtf_enabled']
        del stock['isin']
        del stock['mchart']

    return tempres
