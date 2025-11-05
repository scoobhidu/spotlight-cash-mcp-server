from fastapi import APIRouter, Request
import requests

from config import DATA_API_HOST
from headers_util import add_vensec_auth_to_headers

researchRouter = APIRouter()

@researchRouter.get('/research/equities_investment')
@researchRouter.post('/research/equities_investment')
async def get_research_equities(request: Request):
    url = f"{DATA_API_HOST}/research/investing/v1/equities/"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    payload = {
        "calls": 1,               # e.g. 1
        "sort": 1,                 # e.g. 1
        "start_dt": body["start_dt"],                 # e.g. 2025-02-21
        "end_dt": body["end_dt"],                     # e.g. 2025-08-20
        "page": body.get('page'),                 # e.g. 1
        "size": 30
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    for research in tempres['result']:
        del research['rid']

        research['nse_token'] = research['tkn']
        del research['tkn']

        research['upside'] = research['up_pot']
        del research['up_pot']

        research['vision'] = research['tags']
        del research['tags']

        research['holding_duration'] = research['hld_h']
        del research['hld_h']

        del research['qty']
        del research['exp_prf']

        del research['close_date']
        del research['cls_prc']
        del research['doc_typ']
        del research['value']

        research['scrip_type'] = research['rec_opt']
        del research['rec_opt']

        research['research_doc_url'] = research['url']
        del research['url']

        if research['sl'] == 0 or research['sl'] is None:
            del research['sl']

        if research['exp_dt'] is None:
            del research['exp_dt']

    return tempres

@researchRouter.get('/research/quarterly_results')
@researchRouter.post('/research/quarterly_results')
async def get_research_quarterly(request: Request):
    url = f"{DATA_API_HOST}/research/results/v1/quarterly"

    # Add Ventura Securities auth headers (session_id, x-client-id, Authorization)
    headers = add_vensec_auth_to_headers(
        request.headers.get('session_id'),
        request.headers.get('x-client-id'),
        request.headers.get('Authorization')
    )

    body = await request.json()
    payload = {
        "page": body['page'],          # e.g. 2
        "size": 30,         # e.g. 10
        "fincode": "100209",
        "date_year": body.get("date_year")    # e.g. 202212
    }

    resp = requests.post(url, headers=headers, json=payload)

    tempres = resp.json()

    for research in tempres['result']:
        del research['rid']
        del research['fin']
        del research['doc_typ']

        if research['exp_dt'] is None:
            del research['exp_dt']

        research['quarter'] = research['qtr']
        del research['qtr']

        research["sales"]["value"] = f"{research['sales']['qtr']} Crores"
        del research["sales"]["qtr"]

        research["net_p"]["value"] = f"{research['net_p']['qtr']} Crores"
        del research["net_p"]["qtr"]

        research["net_p"]["qoq"] = f"{research['net_p']['qoq']}%"
        research["net_p"]["yoy"] = f"{research['net_p']['yoy']}%"

        research['net_profit'] = research['net_p']
        del research['net_p']

        research["sales"]["qoq"] = f"{research['sales']['qoq']}%"
        research["sales"]["yoy"] = f"{research['sales']['yoy']}%"

        research['result_month'] = research['date']
        del research['date']

        if research['url'] is not None:
            research['research_doc_url'] = research['url']
        del research['url']

        if research['100_dma'] is None:
            del research['100_dma']

        research['price_earning_ratio'] = research['pe']
        del research['pe']

    return tempres


@researchRouter.get('/research/trading_equities')
@researchRouter.post('/research/trading_equities')
async def get_research_trading_equities(request: Request):
    url = f"{DATA_API_HOST}/research/trading/v1/equities/"

    # Add Ventura Securities auth headers (session_id, x-client-id, Authorization)
    headers = add_vensec_auth_to_headers(
        request.headers.get('session_id'),
        request.headers.get('x-client-id'),
        request.headers.get('Authorization')
    )

    body = await request.json()
    payload = {
        "calls": 1,                # e.g. 1
        "sort": 1,                  # e.g. 1
        "start_dt": body.get("start_dt"),             # e.g. "2025-08-13"
        "end_dt": body.get("end_dt"),                 # e.g. "2025-08-20"
        "page": body.get('page'),                  # e.g. 1
        "size": 30                  # e.g. 10
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    for research in tempres['result']:
        del research['rid']

        research['nse_token'] = research['tkn']
        del research['tkn']

        research['vision'] = research['tags']
        del research['tags']

        del research['qty']
        research['expected_profit'] = research['exp_prf']
        del research['exp_prf']
        research['potential_loss'] = research['p_loss']
        del research['p_loss']

        del research['close_date']
        del research['cls_prc']
        del research['doc_typ']
        del research['value']

        research['scrip_type'] = research['rec_opt']
        del research['rec_opt']

        research['research_doc_url'] = research['url']
        del research['url']

        if research['sl'] == 0 or research['sl'] is None:
            del research['sl']

        if research['prev_target_prc'] is None:
            del research['prev_target_prc']
        if research['prev_recom_prc'] is None:
            del research['prev_recom_prc']
        if research['cls_dt'] is None:
            del research['cls_dt']

    return tempres


@researchRouter.get('/research/trading_options')
@researchRouter.post('/research/trading_options')
async def get_research_trading_options(request: Request):
    url = f"{DATA_API_HOST}/research/trading/v2/options"

    # Add Ventura Securities auth headers (session_id, x-client-id, Authorization)
    headers = add_vensec_auth_to_headers(
        request.headers.get('session_id'),
        request.headers.get('x-client-id'),
        request.headers.get('Authorization')
    )

    body = await request.json()
    payload = {
        "calls": body.get("calls", 1),            # e.g. 1
        "sort": body.get("sort", 1),              # e.g. 1
        "start_dt": body.get("start_dt"),         # e.g. "2025-08-13"
        "end_dt": body.get("end_dt"),             # e.g. "2025-08-20"
        "page": body.get("page", 1),              # e.g. 1
        "size": body.get("size", 10)              # e.g. 10
    }

    resp = requests.post(url, headers=headers, json=payload)
    tempres = resp.json()

    for research in tempres['result']:
        del research['rid']
        del research['tkn']

        research['sym'] += f" {research['opt_typ']}"

        research['vision'] = research['tags']
        del research['tags']

        del research['opt_typ']

        research['expected_profit'] = research['exp_prf']
        del research['exp_prf']
        research['potential_loss'] = research['p_loss']
        del research['p_loss']

        del research['close_date']
        del research['cls_prc']
        del research['doc_typ']
        del research['value']

        research['scrip_type'] = research['rec_opt']
        del research['rec_opt']

        research['research_doc_url'] = research['url']
        del research['url']

        if research['sl'] == 0 or research['sl'] is None:
            del research['sl']

        if research['prev_target_prc'] is None:
            del research['prev_target_prc']
        if research['prev_recom_prc'] is None:
            del research['prev_recom_prc']
        if research['cls_dt'] is None:
            del research['cls_dt']

    return tempres