import requests
from fastapi import APIRouter, Request

from config import DATA_API_HOST
from headers_util import add_vensec_auth_to_headers

ledgerRouter = APIRouter()


@ledgerRouter.get('/last_working_day')
@ledgerRouter.post('/last_working_day')
async def last_working_day(request: Request):
    url = f"{DATA_API_HOST}/stocks/calendar/v1/last_mkt_date"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    return tempres


@ledgerRouter.post('/ledger_reports')
async def get_ledger(request: Request):
    url = "https://settlements.ventura1.com/api/MvpApi/GetLedger"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    payload = {
        "ClientCode": request.headers.get("x-client-id"),
        "FromDate": body["from_date"], # 19-Aug-25
        "ToDate": body["to_date"],
        "Exchange": "All",
        "MtfExclude": 2,
        "UserKey": "15be76482ccf443b41cb3ca66cb025b3e7048ac6",
        "Session_id": request.headers.get("session_id"),
        "Xapikey": request.headers.get("x-api-key", "HKnglr0pyy46BiXiABbZr4DzOXOXtDwA8ljbotJ2"),
        "Authorization": request.headers.get("Authorization"),
        "SSOVerString": "PV5"
    }

    response = requests.post(url, headers=headers, json=payload)
    tempres = response.json()

    for report in tempres:
        del report["SrNo"]
        del report["Vtype"]
        del report["Exchange"]

        if 'BillNo:' in report['DESCRIPTION']:
            report['ledger_detail_id'] = report['DESCRIPTION'].split('BillNo:')[1].split(' ')[0]

        if report['Date'] == "":
            del report['Date']

    return tempres

@ledgerRouter.post('/ledger_bill_details')
async def get_bill_details(request: Request):
    url = "https://settlements.ventura1.com/api/MvpApi/GetMVPBillDetails"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # Build payload dynamically from headers
    payload = {
        "sbillno": body["sbillno"],
        "sparty": request.headers.get("x-client-id", ""),
        "UserKey": "15be76482ccf443b41cb3ca66cb025b3e7048ac6",
        "Session_id": request.headers.get("session_id", ""),
        "Xapikey": "HKnglr0pyy46BiXiABbZr4DzOXOXtDwA8ljbotJ2",
        "Authorization": request.headers.get("Authorization", ""),
        "SSOVerString": "PV5"
    }

    response = requests.post(url, headers=headers, json=payload)
    tempres = response.json()

    for bill in tempres:
        del bill["MktType"]
        del bill["Bkgs"]
        del bill["SetNo"]
        del bill["CfBf"]
        del bill["Exchange"]

        if bill['MktRate'] == 0:
            del bill['MktRate']

        if bill["BS"] == "B":
            bill["action"] = "BUY"
        else:
            bill["action"] = "SELL"

        del bill["BS"]

    return tempres


@ledgerRouter.post('/email_ledger_reports')
async def email_ledger_reports(request: Request):
    url = "{DATA_API_HOST}/backoffice/v1/reports"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    headers["ssoverstring"] = request.headers.get("ssoverstring", "PV5")

    body = await request.json()

    payload = {
        "client_id": request.headers.get("x-client-id"),
        "report": "Get Ledger",
        "format": "xlsx",
        "action": "email",
        "data": {
            "FromDate": body["from_date"],       # e.g. 18-Aug-25
            "ToDate": body["to_date"],           # e.g. 18-Aug-25
            "Segment": None,
            "option": None,
            "beneficiaryac": None,
            "fromval": None,
            "toval": None,
            "scripname": None,
            "Exchange": "All",
            "MtfExclude": 1
        },
        "user_key": "15be76482ccf443b41cb3ca66cb025b3e7048ac6"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


@ledgerRouter.post('/holding_trade_details')
async def get_holding_trade_details(request: Request):
    url = "https://settlements.ventura1.com/api/MvpApi/GetMVPHoldingTradeDetails"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()

    payload = {
        "Clientcode": request.headers.get("x-client-id"),   # e.g. AA0793
        "isin": body["isin"],                  # e.g. INE377Y01014
        "UserKey": "15be76482ccf443b41cb3ca66cb025b3e7048ac6",
        "Session_id": request.headers.get("session_id", ""),
        "Xapikey": "HKnglr0pyy46BiXiABbZr4DzOXOXtDwA8ljbotJ2",
        "Authorization": request.headers.get("Authorization", "Bearer"),
        "SSOVerString": "PV5"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


@ledgerRouter.post('/download_holding_reports')
async def download_holding_reports(request: Request):
    url = "{DATA_API_HOST}/backoffice/v1/reports"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    headers["ssoverstring"] = request.headers.get("ssoverstring", "PV5")

    payload = {
        "client_id": request.headers.get("x-client-id"),
        "report": request.headers.get("report", "Holding Summary"),   # e.g. "Get Ledger"
        "format": request.headers.get("format", "xlsx"),        # e.g. "xlsx"
        "action": request.headers.get("action", "download"),       # e.g. "email"
        "data": {
            "FromDate": "",
            "ToDate": "",
            "Segment": None,
            "option": None,
            "beneficiaryac": None,
            "fromval": None,
            "toval": None,
            "scripname": None,
            "Exchange": None,
            "MtfExclude": None
        },
        "user_key": "15be76482ccf443b41cb3ca66cb025b3e7048ac6"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


@ledgerRouter.post('/trade_reports_summary')
async def get_trade_summary(request: Request):
    url = "https://settlements.ventura1.com/api/MvpApi/GetMVPTradeSummary"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # Build payload dynamically from headers
    payload = {
        "Clientcode": request.headers.get("x-client-id"),
        "FromTrdDate": body["from_date"],
        "ToTrdDate": body["to_date"],
        "Segment":   body["segment"] if 'segment' in body else "Equity",
        "Session_id": request.headers.get("session_id", ""),
        "Xapikey": "HKnglr0pyy46BiXiABbZr4DzOXOXtDwA8ljbotJ2",
        "Authorization": request.headers.get("Authorization", "Bearer"),
        "UserKey": "15be76482ccf443b41cb3ca66cb025b3e7048ac6",
        "SSOVerString": "PV5"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


@ledgerRouter.post('/trade_details_report')
async def get_trade_details(request: Request):
    url = "https://settlements.ventura1.com/api/MvpApi/GetMVPTradeDetails"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    # Build payload dynamically from headers
    payload = {
        "FromTrdDate": body["from_date"],   # e.g. 18-Aug-25
        "ToTrdDate": body["to_date"],       # e.g. 18-Aug-25
        "ClientCode": request.headers.get("x-client-id"),    # e.g. AA0793
        "ScripCode": body["scrip_code"],        # e.g. 532822
        "UserKey": "15be76482ccf443b41cb3ca66cb025b3e7048ac6",
        "Session_id": request.headers.get("session_id", ""),
        "Xapikey": "HKnglr0pyy46BiXiABbZr4DzOXOXtDwA8ljbotJ2",
        "Authorization": request.headers.get("Authorization", "Bearer"),
        "Exchange": request.headers.get("exchange", "NSE"),
        "SSOVerString": "PV5"
    }

    response = requests.post(url, headers=headers, json=payload)
    tempres = response.json()

    for detail in tempres:
        if detail['BS'] == "B":
            detail['action'] = "BUY"
        else:
            detail['action'] = "SELL"
        del detail['BS']

    return tempres


@ledgerRouter.post('/email_trade_reports')
async def email_trade_reports(request: Request):
    url = "{DATA_API_HOST}/backoffice/v1/reports"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    headers["ssoverstring"] = request.headers.get("ssoverstring", "PV5")

    body = await request.json()
    payload = {
        "client_id": request.headers.get("x-client-id"),
        "report": "Trade Summary",
        "format": "xlsx",
        "action": "email",
        "data": {
            "FromDate": body["from_date"],
            "ToDate": body["to_date"],
            "Segment": None,
            "option": None,
            "beneficiaryac": None,
            "fromval": None,
            "toval": None,
            "scripname": None,
            "Exchange": None,
            "MtfExclude": None
        },
        "user_key": "15be76482ccf443b41cb3ca66cb025b3e7048ac6"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


@ledgerRouter.post('/get_tax_reports')
async def get_tax_reports(request: Request):
    url = "https://settlements.ventura1.com/api/MvpApi/GetMVPPortfolioReport"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    body = await request.json()
    payload = {
        "Clientcode": request.headers.get("x-client-id"),     # e.g. 97993272
        "FromDate": body["from_date"],           # e.g. 01-Apr-25
        "ToDate": body["to_date"],               # e.g. 31-Mar-26
        "UserKey": "15be76482ccf443b41cb3ca66cb025b3e7048ac6",
        "Session_id": request.headers.get("session_id", ""),
        "Xapikey": request.headers.get("x-api-key", ""),
        "Authorization": request.headers.get("Authorization", "Bearer"),
        "SSOVerString": "PV5",
    }

    resp = requests.post(url, headers=headers, json=payload)
    return resp.json()


@ledgerRouter.post('/email_tax_reports')
async def email_tax_reports(request: Request):
    url = "{DATA_API_HOST}/backoffice/v1/reports"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    headers["ssoverstring"] = request.headers.get("ssoverstring", "PV5")

    body = await request.json()
    payload = {
        "client_id": request.headers.get("x-client-id"),
        "report": "Tax Report",
        "format": "xlsx",
        "action": "email",
        "data": {
            "FromDate": body["from_date"],
            "ToDate": body["to_date"],
            "Segment": "Equity",
            "option": None,
            "beneficiaryac": None,
            "fromval": None,
            "toval": None,
            "scripname": None,
            "Exchange": None,
            "MtfExclude": None
        },
        "user_key": "15be76482ccf443b41cb3ca66cb025b3e7048ac6"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


@ledgerRouter.post('/email_contract_notes')
async def email_contract_notes(request: Request):
    url = "https://support-fastapi.venturasecurities.com/support/v1/user/ticket/create"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    headers["x-api-key"] = "DcwqYxFLlIBEJWIXvSL7XA0SsLN8sDYIGJFIF1DIOa6e8N7"

    body = await request.json()

    payload = {
        "client_id": request.headers.get("x-client-id"),  # e.g. AA0793
        "product_id": "1",
        "question_id": "155",
        "category_id": "2",
        "query": f"Contract note for AA0793 dated {body['from_date']} To {body['to_date']}",  # e.g. "Contract note ..."
        "subject": "Contract Note",
        "file_data": ""
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


@ledgerRouter.post('/email_daily_activity_statement')
async def email_daily_activity_statement(request: Request):
    url = "https://support-fastapi.venturasecurities.com/support/v1/user/ticket/create"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))
    headers["x-api-key"] = "DcwqYxFLlIBEJWIXvSL7XA0SsLN8sDYIGJFIF1DIOa6e8N7"

    body = await request.json()
    payload = {
        "client_id": request.headers.get("x-client-id"),  # e.g. AA0793
        "product_id": "1",
        "question_id": "119",
        "category_id": "2",
        "query": f"Daily Activity Statement for AA0793 dated {body['from_date']}",  # e.g. "Contract note ..."
        "subject": "Daily Activity Statement",
        "file_data": ""
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


@ledgerRouter.post('/get_dividend_report')
async def get_dividend_report(request: Request):
    url = "{DATA_API_HOST}/backoffice/v1/beneficiaryac"

    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'), request.headers.get('Authorization'))

    payload = {
        "client_id": request.headers.get("x-client-id")
    }

    response = requests.post(url, headers=headers, json=payload)
    beneficiary_ac = response.json()['response']['Table'][0]['beneficiaryac']

    # Step 2: Call dividend API using beneficiary account
    div_url = "{DATA_API_HOST}/backoffice/v1/dividend"
    headers["ocrapikey"] = request.headers.get("ocrapikey", "OCRID5:4UESfSQpwztQfAw0ho3mlb5teQuindEW")

    body = await request.json()
    div_payload = {
        "option": body["option"] if "option" in body else "finwise",
        "beneficiaryac": beneficiary_ac,
        "fromval": body["from_year"] if 'from_year' in body else "2025-2026",
        "toval": "",
        "scripname": "",
        "session_id": None,
        "client_id": request.headers.get("x-client-id"),
        "token": None
    }
    div_res = requests.post(div_url, headers=headers, json=div_payload).json()

    return div_res
