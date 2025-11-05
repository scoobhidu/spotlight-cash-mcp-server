from fastapi import APIRouter, Request
import requests

from headers_util import add_vensec_auth_to_headers

ipoRouter = APIRouter()

@ipoRouter.get('/ipo/ongoing')
async def get_ipo_ongoing(request: Request):
    url = "https://ipo2-api.venturasecurities.com/ipo/v2/ongoing"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    headers["x-api-key"] = request.headers.get("x-api-key", "Tz2Wez1c7O6NwWrzyjwP6vRfsHeRVDI6oDP1zlgh")

    response = requests.get(url, headers=headers)
    tempres = response.json()

    for ipo in tempres['data']:
        ipo['ipo_code'] = ipo['accord_ipo_code']
        del ipo['accord_ipo_code']
        del ipo['ipo_id']
        del ipo['logo']

        ipo['ipo_issue_price'] = ipo['price_range_high']
        del ipo['price_range_high']
        del ipo['min_lot_size']
        del ipo['min_issue_size']

        ipo['max_issue_size'] = f"{ipo['max_issue_size']} Crores"
        ipo['research_report'] = ipo['drhp']
        del ipo['drhp']

        del ipo['pre_apply']
        del ipo['bid_quantity']
        del ipo['symbol']
        del ipo['investor_category_type']
        del ipo['investor_category_id']
        del ipo['discount_amount_per_share']
        del ipo['min_investment']

        ipo['min_investment_amount'] = f"{ipo['total_amount']}"
        del ipo['total_amount']

        ipo['subscription'] = f'{ipo["subscription"]} x'

    return tempres

@ipoRouter.get('/ipo/details')
async def get_ipo_details(request: Request):
    url = f"https://ipo2-api.venturasecurities.com/ipo/v1/company/details?accord_ipo_code={request.query_params.get('ipo_code')}"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    headers["x-api-key"] = request.headers.get("x-api-key", "Tz2Wez1c7O6NwWrzyjwP6vRfsHeRVDI6oDP1zlgh")

    response = requests.get(url, headers=headers)
    tempres = response.json()

    data = {}
    if 'revenue' in tempres and tempres['revenue'] is not None:
        data['revenue'] = tempres['revenue']
    if 'total_assets' in tempres and tempres['total_assets'] is not None:
        data['total_assets'] = tempres['total_assets']
    if 'profit' in tempres and tempres['profit'] is not None:
        data['profit'] = tempres['profit']

    if 'post_listing_mcap' in tempres and tempres['post_listing_mcap'] is not None:
        data['post_listing_mcap'] = tempres['post_listing_mcap']
    if 'promoter_pct_change' in tempres and tempres['promoter_pct_change'] is not None:
        data['promoter_pct_change'] = tempres['promoter_pct_change']

    if 'list_price' in tempres and tempres['list_price'] is not None:
        data['list_price'] = tempres['list_price']
    if 'pct_change' in tempres and tempres['pct_change'] is not None:
        data['pct_change'] = tempres['pct_change']
    if 'price_difference' in tempres and tempres['price_difference'] is not None:
        data['price_difference'] = tempres['price_difference']

    return data

@ipoRouter.get('/ipo/closed')
async def get_ipo_ongoing(request: Request):
    url = "https://ipo2-api.venturasecurities.com/ipo/v2/closed"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    headers["x-api-key"] = request.headers.get("x-api-key", "Tz2Wez1c7O6NwWrzyjwP6vRfsHeRVDI6oDP1zlgh")

    response = requests.get(url, headers=headers)
    return response.json()


@ipoRouter.get('/ipo/listed')
async def get_ipo_ongoing(request: Request):
    url = "https://ipo2-api.venturasecurities.com/ipo/v2/listed"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    headers["x-api-key"] = request.headers.get("x-api-key", "Tz2Wez1c7O6NwWrzyjwP6vRfsHeRVDI6oDP1zlgh")

    response = requests.get(url, headers=headers)
    tempres = response.json()

    for ipo in tempres['data']:
        ipo['ipo_code'] = ipo['accord_ipo_code']
        del ipo['accord_ipo_code']
        del ipo['ipo_id']
        del ipo['logo']

        ipo['ipo_issue_price'] = ipo['price_range_high']
        del ipo['price_range_high']
        del ipo['min_lot_size']
        del ipo['min_issue_size']

        ipo['max_issue_size'] = f"{ipo['max_issue_size']} Crores"
        ipo['research_report'] = ipo['drhp']
        del ipo['drhp']

        del ipo['bid_quantity']
        del ipo['symbol']
        del ipo['investor_category_type']
        del ipo['investor_category_id']
        del ipo['min_investment']

        ipo['subscription'] = f'{ipo["subscription"]} x'

    return tempres


