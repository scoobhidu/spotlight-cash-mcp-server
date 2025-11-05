from fastapi import APIRouter, Request
import requests

from config import DATA_API_HOST
from headers_util import add_vensec_auth_to_headers

fnoRouter = APIRouter()

@fnoRouter.get('/futuremovers/indices/oigainer')
@fnoRouter.post('/futuremovers/indices/oigainer')
async def get_futuremovers_indices_oigainer(request: Request):
    url = f"{DATA_API_HOST}/fno/futuremovers/indices/v2/oigainer"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            if gainer['strike_price'] == "-1":
                del gainer['strike_price']

    return tempres


@fnoRouter.get('/futuremovers/indices/oiloser')
@fnoRouter.post('/futuremovers/indices/oiloser')
async def get_futuremovers_indices_oilosers(request: Request):
    url = f"{DATA_API_HOST}/fno/futuremovers/indices/v2/oiloser"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            if gainer['strike_price'] == "-1":
                del gainer['strike_price']

    return tempres


@fnoRouter.get('/futuremovers/indices/pricegainer')
@fnoRouter.post('/futuremovers/indices/pricegainer')
async def get_futuremovers_indices_pricegainer(request: Request):
    url = f"{DATA_API_HOST}/fno/futuremovers/indices/v2/pricegainer"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            if gainer['strike_price'] == "-1":
                del gainer['strike_price']

    return tempres

@fnoRouter.get('/futuremovers/indices/priceloser')
@fnoRouter.post('/futuremovers/indices/priceloser')
async def get_futuremovers_indices_priceloser(request: Request):
    url = f"{DATA_API_HOST}/fno/futuremovers/indices/v2/pricegainer"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            if gainer['strike_price'] == "-1":
                del gainer['strike_price']

    return tempres


@fnoRouter.get('/futuremovers/indices/oianalysis')
@fnoRouter.post('/futuremovers/indices/oianalysis')
async def get_futuremovers_indices_oianalysis(request: Request):
    url = f"{DATA_API_HOST}/fno/futuremovers/indices/v2/oianalysis"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    payload = {
        "oi_type": body.get('type'),
        "page": 0,
        "size": 30
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            if gainer['strike_price'] == "-1":
                del gainer['strike_price']

    return tempres







@fnoRouter.get('/futuremovers/stocks/activevol')
@fnoRouter.post('/futuremovers/stocks/activevol')
async def get_futuremovers_stocks_activevol(request: Request):
    url = f"{DATA_API_HOST}/fno/futuremovers/stocks/v2/actvol"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            if gainer['strike_price'] == "-1":
                del gainer['strike_price']

    return tempres

@fnoRouter.get('/futuremovers/stocks/oigainer')
@fnoRouter.post('/futuremovers/stocks/oigainer')
async def get_futuremovers_stocks_oigainer(request: Request):
    url = f"{DATA_API_HOST}/fno/futuremovers/stocks/v2/oigainer"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            if gainer['strike_price'] == "-1":
                del gainer['strike_price']

    return tempres


@fnoRouter.get('/futuremovers/stocks/oiloser')
@fnoRouter.post('/futuremovers/stocks/oiloser')
async def get_futuremovers_stocks_oiloser(request: Request):
    url = f"{DATA_API_HOST}/fno/futuremovers/stocks/v2/oiloser"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            if gainer['strike_price'] == "-1":
                del gainer['strike_price']

    return tempres


@fnoRouter.get('/futuremovers/stocks/pricegainer')
@fnoRouter.post('/futuremovers/stocks/pricegainer')
async def get_futuremovers_stocks_pricegainer(request: Request):
    url = f"{DATA_API_HOST}/fno/futuremovers/stocks/v2/pricegainer"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            if gainer['strike_price'] == "-1":
                del gainer['strike_price']

    return tempres


@fnoRouter.get('/futuremovers/stocks/priceloser')
@fnoRouter.post('/futuremovers/stocks/priceloser')
async def get_futuremovers_stocks_priceloser(request: Request):
    url = f"{DATA_API_HOST}/fno/futuremovers/stocks/v2/pricegainer"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            if gainer['strike_price'] == "-1":
                del gainer['strike_price']

    return tempres


@fnoRouter.get('/futuremovers/stocks/oianalysis')
@fnoRouter.post('/futuremovers/stocks/oianalysis')
async def get_futuremovers_stocks_oianalysis(request: Request):
    url = f"{DATA_API_HOST}/fno/futuremovers/stocks/v2/oianalysis"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()

    payload = {
        "oi_type": body.get('type'),
        "page": 0,
        "size": 30
    }

    resp = requests.post(url, headers=headers, json=payload)

    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            if gainer['strike_price'] == "-1":
                del gainer['strike_price']

    return tempres



############# OPTIONS ############



@fnoRouter.get('/optmovers/stocks/activevol')
@fnoRouter.post('/optmovers/stocks/activevol')
async def optmovers_stocks_activevol(request: Request):
    url = f"{DATA_API_HOST}/fno/optionmovers/stocks/v2/actvol"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['strike_price']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            del gainer['strike_price']

    return tempres

@fnoRouter.get('/optmovers/stocks/oigainer')
@fnoRouter.post('/optmovers/stocks/oigainer')
async def optmovers_stocks_oigainer(request: Request):
    url = f"{DATA_API_HOST}/fno/optionmovers/stocks/v2/oigainer"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['strike_price']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            del gainer['strike_price']

        return tempres


@fnoRouter.get('/optmovers/stocks/oiloser')
@fnoRouter.post('/optmovers/stocks/oiloser')
async def optmovers_stocks_oiloser(request: Request):
    url = f"{DATA_API_HOST}/fno/optionmovers/stocks/v2/oiloser"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()


    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['strike_price']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            del gainer['strike_price']

    return tempres


@fnoRouter.get('/optmovers/stocks/pricegainer')
@fnoRouter.post('/optmovers/stocks/pricegainer')
async def optmovers_stocks_pricegainer(request: Request):
    url = f"{DATA_API_HOST}/fno/optionmovers/stocks/v2/pricegainer"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['strike_price']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            del gainer['strike_price']

    return tempres


@fnoRouter.get('/optmovers/stocks/priceloser')
@fnoRouter.post('/optmovers/stocks/priceloser')
async def optmovers_stocks_oigainer(request: Request):
    url = f"{DATA_API_HOST}/fno/optionmovers/stocks/v2/pricegainer"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['strike_price']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            del gainer['strike_price']

    return tempres







@fnoRouter.get('/optmovers/indices/activevol')
@fnoRouter.post('/optmovers/indices/activevol')
async def optmovers_indices_activevol(request: Request):
    url = f"{DATA_API_HOST}/fno/optionmovers/indices/v2/actvol"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['strike_price']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            del gainer['strike_price']

    return tempres


@fnoRouter.get('/optmovers/indices/oigainer')
@fnoRouter.post('/optmovers/indices/oigainer')
async def indices_optmovers_oigainer(request: Request):
    url = f"{DATA_API_HOST}/fno/optionmovers/indices/v2/oigainer"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['strike_price']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            del gainer['strike_price']

    return tempres


@fnoRouter.get('/optmovers/indices/oiloser')
@fnoRouter.post('/optmovers/indices/oiloser')
async def indices_optmovers_oiloser(request: Request):
    url = f"{DATA_API_HOST}/fno/optionmovers/indices/v2/oiloser"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['strike_price']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            del gainer['strike_price']

    return tempres


@fnoRouter.get('/optmovers/indices/pricegainer')
@fnoRouter.post('/optmovers/indices/pricegainer')
async def indices_optmovers_pricegainer(request: Request):
    url = f"{DATA_API_HOST}/fno/optionmovers/indices/v2/pricegainer"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['strike_price']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            del gainer['strike_price']

    return tempres


@fnoRouter.get('/optmovers/indices/priceloser')
@fnoRouter.post('/optmovers/indices/priceloser')
async def indices_optmovers_priceloser(request: Request):
    url = f"{DATA_API_HOST}/fno/optionmovers/indices/v2/pricegainer"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # default payload; can be overridden by client headers if needed
    payload = {
        "expiry_type": body.get("expiry_type"),  # e.g. M1
        "page": 0,              # e.g. 0
        "size": 30              # e.g. 15
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    if 'result' not in tempres or len(tempres['result']) == 0:
        return {}
    else:
        for gainer in tempres['result']:
            gainer['volume'] = gainer['v']
            del gainer['v']
            del gainer['expiry_type']
            del gainer['expiry_date']

            gainer['nci'] += "%"

            gainer['sym'] += f" {gainer['fdate']} {gainer['strike_price']} {gainer['op_type']}"

            del gainer['fdate']
            del gainer['op_type']

            gainer['oi_change'] = gainer['oi_nci'] + "%"
            del gainer['oi_nci']

            gainer['volume_change'] = gainer['v_nci'] + "%"
            del gainer['v_nci']

            gainer['previous_oi'] = gainer['p_oi']
            del gainer['p_oi']

            gainer['previous_volume'] = gainer['p_vol']
            del gainer['p_vol']

            gainer['optionchain_spot_token'] = gainer['oc_token']
            del gainer['oc_token']
            del gainer['mchart']

            del gainer['strike_price']

    return tempres

@fnoRouter.get('/banlist')
@fnoRouter.post('/banlist')
async def banlist(request: Request):
    url = f"{DATA_API_HOST}/fno/v1/banlist"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    resp = requests.get(url, headers=headers)
    return resp.json()
