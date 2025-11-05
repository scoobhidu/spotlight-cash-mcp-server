import requests
from fastapi import APIRouter, Request

from config import master, DATA_API_HOST
from headers_util import add_niftytrader_auth_to_headers, add_vensec_auth_to_headers

finRouter = APIRouter()

class StockFinancials:
    def __init__(self, clientid, sessionid, authorization):
        self.clientid = clientid
        self.sessionid = sessionid
        self.auth = authorization

    async def GetFinancialSummary(self, res):
        for h in res['user_portfolio']['holdings']:
            url = f"{DATA_API_HOST}/stocks/fundamental/financial/v1/all?token={h}"
            headers = add_vensec_auth_to_headers(self.sessionid,self.clientid,self.auth)

            response = requests.request("GET", url, headers=headers, data={})
            tempres = response.json()

            res['user_portfolio']['holdings'][h]['company_financials'] = {}
            res['user_portfolio']['holdings'][h]['company_financials']['nudge'] = 'All the company_financials data is in crore rupees scale'
            if 'bal_c' in tempres:
                res['user_portfolio']['holdings'][h]['company_financials']['consolidated_balance_sheet_yoy'] = tempres['bal_c']
            if 'bal_s' in tempres:
                res['user_portfolio']['holdings'][h]['company_financials']['standalone_balance_sheet_yoy'] = tempres['bal_s']
            if 'cf_c' in tempres:
                res['user_portfolio']['holdings'][h]['company_financials']['consolidated_cash_flow_statement_yoy'] = tempres['cf_c']
            if 'cf_s' in tempres:
                res['user_portfolio']['holdings'][h]['company_financials']['standalone_cash_flow_statement_yoy'] = tempres['cf_s']

            if 'fin_r_c' in tempres:
                if 'nt_prt_mrg' in tempres['fin_r_c']:
                    tempres['fin_r_c']['net_profit_margin'] = tempres['fin_r_c']['nt_prt_mrg']
                    del tempres['fin_r_c']['nt_prt_mrg']

                if 'op_prt_mrg' in tempres['fin_r_c']:
                    tempres['fin_r_c']['operational_profit_margin'] = tempres['fin_r_c']['op_prt_mrg']
                    del tempres['fin_r_s']['nt_prt_mrg']

                res['user_portfolio']['holdings'][h]['company_financials']['condolidated_financial_ratios'] = tempres['fin_r_c']

            if 'fin_r_s' in tempres:
                if 'nt_prt_mrg' in tempres['fin_r_s']:
                    tempres['fin_r_s']['net_profit_margin'] = tempres['fin_r_s']['nt_prt_mrg']
                    del tempres['fin_r_c']['op_prt_mrg']

                if 'op_prt_mrg' in tempres['fin_r_s']:
                    tempres['fin_r_s']['operational_profit_margin'] = tempres['fin_r_s']['op_prt_mrg']
                    del tempres['fin_r_s']['op_prt_mrg']

                res['user_portfolio']['holdings'][h]['company_financials']['standalone_financial_ratios'] = tempres['fin_r_s']

            if 'op_c' in tempres:
                if 'curr_ratio' in tempres['op_c']:
                    tempres['op_c']['current_ratio'] = tempres['op_c']['curr_ratio']
                    del tempres['op_c']['curr_ratio']

                if 'd_to_e' in tempres['op_c']:
                    tempres['op_c']['debt_to_eq'] = tempres['op_c']['d_to_e']
                    del tempres['op_c']['d_to_e']

                if 'int_coverage' in tempres['op_c']:
                    tempres['op_c']['international_coverage'] = tempres['op_c']['int_coverage']
                    del tempres['op_c']['int_coverage']

                if 'qr' in tempres['op_c']:
                    tempres['op_c']['quick_ratio'] = tempres['op_c']['qr']
                    del tempres['op_c']['qr']

                if 'turnover' in tempres['op_c']:
                    tempres['op_c']['assets_turnover'] = tempres['op_c']['turnover']
                    del tempres['op_c']['turnover']

                res['user_portfolio']['holdings'][h]['company_financials']['consolidated_operational_ratios'] = tempres['op_c']

            if 'op_s' in tempres:
                if 'curr_ratio' in tempres['op_s']:
                    tempres['op_s']['current_ratio'] = tempres['op_s']['curr_ratio']
                    del tempres['op_s']['curr_ratio']

                if 'd_to_e' in tempres['op_s']:
                    tempres['op_s']['debt_to_eq'] = tempres['op_s']['d_to_e']
                    del tempres['op_s']['d_to_e']

                if 'int_coverage' in tempres['op_s']:
                    tempres['op_s']['international_coverage'] = tempres['op_s']['int_coverage']
                    del tempres['op_s']['int_coverage']

                if 'qr' in tempres['op_s']:
                    tempres['op_s']['quick_ratio'] = tempres['op_s']['qr']
                    del tempres['op_s']['qr']

                if 'turnover' in tempres['op_s']:
                    tempres['op_s']['assets_turnover'] = tempres['op_s']['turnover']
                    del tempres['op_s']['turnover']

                res['user_portfolio']['holdings'][h]['company_financials']['standalone_operational_ratios'] = tempres['op_s']



            if tempres['qtr_c'] is not None:
                if 'ni' in tempres['qtr_c']:
                    tempres['qtr_c']['net_income'] = {}
                    if len(tempres['qtr_c']['ni']) > 0:
                        tempres['qtr_c']['net_income']['value'] = tempres['qtr_c']['ni'][0]

                    if len(tempres['qtr_c']['ni']) > 1:
                        tempres['qtr_c']['net_income']['percentage_change'] = tempres['qtr_c']['ni'][1]

                    del tempres['qtr_c']['ni']

                if 'op' in tempres['qtr_c']:
                    tempres['qtr_c']['operating_profits'] = {}
                    if len(tempres['qtr_c']['op']) > 0:
                        tempres['qtr_c']['operating_profits']['value'] = tempres['qtr_c']['op'][0]

                    if len(tempres['qtr_c']['op']) > 1:
                        tempres['qtr_c']['operating_profits']['percentage_change'] = tempres['qtr_c']['op'][1]

                    del tempres['qtr_c']['op']

                if 'revenue' in tempres['qtr_c']:
                    tempres['qtr_c']['revenues'] = {}

                    if len(tempres['qtr_c']['revenue']) > 0:
                        tempres['qtr_c']['revenues']['value'] = tempres['qtr_c']['revenue'][0]
                    if len(tempres['qtr_c']['revenue']) > 1:
                        tempres['qtr_c']['revenues']['percentage_change'] = tempres['qtr_c']['revenue'][1]

                    del tempres['qtr_c']['revenue']

                res['user_portfolio']['holdings'][h]['company_financials']['consolidated_quarterly_result'] = tempres['qtr_c']

            if tempres['qtr_s'] is not None:
                if 'ni' in tempres['qtr_s']:
                    tempres['qtr_s']['net_income'] = {}
                    if len(tempres['qtr_s']['ni']) > 0:
                        tempres['qtr_s']['net_income']['value'] = tempres['qtr_s']['ni'][0]

                    if len(tempres['qtr_s']['ni']) > 1:
                        tempres['qtr_s']['net_income']['percentage_change'] = tempres['qtr_s']['ni'][1]

                    del tempres['qtr_s']['ni']

                if 'op' in tempres['qtr_s']:
                    tempres['qtr_s']['operating_profits'] = {}
                    if len(tempres['qtr_s']['op']) > 0:
                        tempres['qtr_s']['operating_profits']['value'] = tempres['qtr_s']['op'][0]

                    if len(tempres['qtr_s']['op']) > 1:
                        tempres['qtr_s']['operating_profits']['percentage_change'] = tempres['qtr_s']['op'][1]

                    del tempres['qtr_s']['op']

                if 'revenue' in tempres['qtr_s']:
                    tempres['qtr_s']['revenues'] = {}

                    if len(tempres['qtr_s']['revenue']) > 0:
                        tempres['qtr_s']['revenues']['value'] = tempres['qtr_s']['revenue'][0]
                    if len(tempres['qtr_s']['revenue']) > 1:
                        tempres['qtr_s']['revenues']['percentage_change'] = tempres['qtr_s']['revenue'][1]

                    del tempres['qtr_s']['revenue']

                res['user_portfolio']['holdings'][h]['company_financials']['standalone_quarterly_result'] = tempres['qtr_s']

        return res

    async def GetStandaloneIncomeStatement(self, res):
        for h in res['user_portfolio']['holdings']:
            url = f"{DATA_API_HOST}/stocks/fundamental/financial/v1/incomestmt/standalone?token={h}&type=A"
            headers = add_vensec_auth_to_headers(self.sessionid,self.clientid,self.auth)

            response = requests.request("GET", url, headers=headers, data={})
            tempres = response.json()

            res['user_portfolio']['holdings'][h]['standalone_company_imcome_statement_yoy'] = {}

            for income in tempres['inc_sat']:
                if 'dt' in income:
                    income['financial_year'] = income['dt']
                    del income['dt']

                if 'ni' in income:
                    income['net_income'] = income['ni']
                    del income['ni']

                if 'op' in income:
                    income['operating_profit'] = income['op']
                    del income['op']


            res['user_portfolio']['holdings'][h]['standalone_company_imcome_statement_yoy'] = tempres['inc_sat']

        return res


    async def GetConsolidatedIncomeStatement(self, res):
        for h in res['user_portfolio']['holdings']:
            url = f"{DATA_API_HOST}/stocks/fundamental/financial/v1/incomestmt/consolidated?token={h}&type=A"
            headers = add_vensec_auth_to_headers(self.sessionid, self.clientid, self.auth)

            response = requests.request("GET", url, headers=headers, data={})
            tempres = response.json()

            res['user_portfolio']['holdings'][h]['consolidated_company_imcome_statement_yoy'] = {}

            if 'inc_sat' in tempres:
                for income in tempres['inc_sat']:
                    income['financial_year'] = income['dt']
                    del income['dt']

                    if 'ni' in income:
                        income['net_income'] = income['ni']
                        del income['ni']

                    if 'op' in income:
                        income['operating_profit'] = income['op']
                        del income['op']

                res['user_portfolio']['holdings'][h]['consolidated_company_imcome_statement_yoy'] = tempres['inc_sat']


    async def GetStandaloneValuation(self, res):
        for h in res['user_portfolio']['holdings']:
            url = f"{DATA_API_HOST}/stocks/fundamental/financial/v1/overview/standalone?token={h}"
            headers = add_vensec_auth_to_headers(self.sessionid, self.clientid, self.auth)

            response = requests.request("GET", url, headers=headers, data={})
            tempres = response.json()
            if 'fv' in tempres:
                res['user_portfolio']['holdings'][h]['stock_face_value'] = tempres['fv']
            if 'bv' in tempres:
                res['user_portfolio']['holdings'][h]['company_book_value'] = tempres['bv']
            if 'yield' in tempres:
                res['user_portfolio']['holdings'][h]['dividend_yield'] = tempres['yield']
            if 'debt_eq' in tempres:
                res['user_portfolio']['holdings'][h]['debt_equity_ratio'] = tempres['debt_eq']
            if 'pb' in tempres:
                res['user_portfolio']['holdings'][h]['price_book_ratio'] = tempres['pb']


@finRouter.get('/get_stock_financial_summary')
@finRouter.post('/get_stock_financial_summary')
async def GetFinancialSummary(request: Request, symbol: str):
    url = f"{DATA_API_HOST}/stocks/fundamental/financial/v1/all?token={master[symbol]}"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'),
                                         request.headers.get('Authorization'))

    response = requests.request("GET", url, headers=headers, data={})
    tempres = response.json()

    res = {'note': 'All the company_financials data is in crore rupees scale'}

    if 'bal_c' in tempres:
        res['consolidated_balance_sheet_yoy'] = tempres['bal_c']
    if 'bal_s' in tempres:
        res['standalone_balance_sheet_yoy'] = tempres['bal_s']
    if 'cf_c' in tempres:
        res['consolidated_cash_flow_statement_yoy'] = tempres[
            'cf_c']
    if 'cf_s' in tempres:
        res['standalone_cash_flow_statement_yoy'] = tempres[
            'cf_s']

    if 'fin_r_c' in tempres:
        if 'nt_prt_mrg' in tempres['fin_r_c']:
            tempres['fin_r_c']['net_profit_margin'] = tempres['fin_r_c']['nt_prt_mrg']
            del tempres['fin_r_c']['nt_prt_mrg']

        if 'op_prt_mrg' in tempres['fin_r_c']:
            tempres['fin_r_c']['operational_profit_margin'] = tempres['fin_r_c']['op_prt_mrg']
            del tempres['fin_r_s']['nt_prt_mrg']

        res['condolidated_financial_ratios'] = tempres['fin_r_c']

    if 'fin_r_s' in tempres:
        if 'nt_prt_mrg' in tempres['fin_r_s']:
            tempres['fin_r_s']['net_profit_margin'] = tempres['fin_r_s']['nt_prt_mrg']
            del tempres['fin_r_c']['op_prt_mrg']

        if 'op_prt_mrg' in tempres['fin_r_s']:
            tempres['fin_r_s']['operational_profit_margin'] = tempres['fin_r_s']['op_prt_mrg']
            del tempres['fin_r_s']['op_prt_mrg']

        res['standalone_financial_ratios'] = tempres['fin_r_s']

    if 'op_c' in tempres:
        if 'curr_ratio' in tempres['op_c']:
            tempres['op_c']['current_ratio'] = tempres['op_c']['curr_ratio']
            del tempres['op_c']['curr_ratio']

        if 'd_to_e' in tempres['op_c']:
            tempres['op_c']['debt_to_eq'] = tempres['op_c']['d_to_e']
            del tempres['op_c']['d_to_e']

        if 'int_coverage' in tempres['op_c']:
            tempres['op_c']['international_coverage'] = tempres['op_c']['int_coverage']
            del tempres['op_c']['int_coverage']

        if 'qr' in tempres['op_c']:
            tempres['op_c']['quick_ratio'] = tempres['op_c']['qr']
            del tempres['op_c']['qr']

        if 'turnover' in tempres['op_c']:
            tempres['op_c']['assets_turnover'] = tempres['op_c']['turnover']
            del tempres['op_c']['turnover']

        res['consolidated_operational_ratios'] = tempres['op_c']

    if 'op_s' in tempres:
        if 'curr_ratio' in tempres['op_s']:
            tempres['op_s']['current_ratio'] = tempres['op_s']['curr_ratio']
            del tempres['op_s']['curr_ratio']

        if 'd_to_e' in tempres['op_s']:
            tempres['op_s']['debt_to_eq'] = tempres['op_s']['d_to_e']
            del tempres['op_s']['d_to_e']

        if 'int_coverage' in tempres['op_s']:
            tempres['op_s']['international_coverage'] = tempres['op_s']['int_coverage']
            del tempres['op_s']['int_coverage']

        if 'qr' in tempres['op_s']:
            tempres['op_s']['quick_ratio'] = tempres['op_s']['qr']
            del tempres['op_s']['qr']

        if 'turnover' in tempres['op_s']:
            tempres['op_s']['assets_turnover'] = tempres['op_s']['turnover']
            del tempres['op_s']['turnover']

        res['standalone_operational_ratios'] = tempres['op_s']

    if tempres['qtr_c'] is not None:
        if 'ni' in tempres['qtr_c']:
            tempres['qtr_c']['net_income'] = {}
            if len(tempres['qtr_c']['ni']) > 0:
                tempres['qtr_c']['net_income']['value'] = tempres['qtr_c']['ni'][0]

            if len(tempres['qtr_c']['ni']) > 1:
                tempres['qtr_c']['net_income']['percentage_change'] = tempres['qtr_c']['ni'][1]

            del tempres['qtr_c']['ni']

        if 'op' in tempres['qtr_c']:
            tempres['qtr_c']['operating_profits'] = {}
            if len(tempres['qtr_c']['op']) > 0:
                tempres['qtr_c']['operating_profits']['value'] = tempres['qtr_c']['op'][0]

            if len(tempres['qtr_c']['op']) > 1:
                tempres['qtr_c']['operating_profits']['percentage_change'] = tempres['qtr_c']['op'][1]

            del tempres['qtr_c']['op']

        if 'revenue' in tempres['qtr_c']:
            tempres['qtr_c']['revenues'] = {}

            if len(tempres['qtr_c']['revenue']) > 0:
                tempres['qtr_c']['revenues']['value'] = tempres['qtr_c']['revenue'][0]
            if len(tempres['qtr_c']['revenue']) > 1:
                tempres['qtr_c']['revenues']['percentage_change'] = tempres['qtr_c']['revenue'][1]

            del tempres['qtr_c']['revenue']

    if tempres['qtr_s'] is not None:
        if 'ni' in tempres['qtr_s']:
            tempres['qtr_s']['net_income'] = {}
            if len(tempres['qtr_s']['ni']) > 0:
                tempres['qtr_s']['net_income']['value'] = tempres['qtr_s']['ni'][0]

            if len(tempres['qtr_s']['ni']) > 1:
                tempres['qtr_s']['net_income']['percentage_change'] = tempres['qtr_s']['ni'][1]

            del tempres['qtr_s']['ni']

        if 'op' in tempres['qtr_s']:
            tempres['qtr_s']['operating_profits'] = {}
            if len(tempres['qtr_s']['op']) > 0:
                tempres['qtr_s']['operating_profits']['value'] = tempres['qtr_s']['op'][0]

            if len(tempres['qtr_s']['op']) > 1:
                tempres['qtr_s']['operating_profits']['percentage_change'] = tempres['qtr_s']['op'][1]

            del tempres['qtr_s']['op']

        if 'revenue' in tempres['qtr_s']:
            tempres['qtr_s']['revenues'] = {}

            if len(tempres['qtr_s']['revenue']) > 0:
                tempres['qtr_s']['revenues']['value'] = tempres['qtr_s']['revenue'][0]
            if len(tempres['qtr_s']['revenue']) > 1:
                tempres['qtr_s']['revenues']['percentage_change'] = tempres['qtr_s']['revenue'][1]

            del tempres['qtr_s']['revenue']

        res['consolidated_quarterly_result'] = tempres['qtr_c']
        res['standalone_quarterly_result'] = tempres['qtr_s']


    return res

@finRouter.get('/get_stock_standalone_income_statement')
@finRouter.post('/get_stock_standalone_income_statement')
async def GetStandaloneIncomeStatement(request: Request, symbol: str):
    url = f"{DATA_API_HOST}/stocks/fundamental/financial/v1/incomestmt/standalone?token={master[symbol]}&type=A"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'),
                                         request.headers.get('Authorization'))

    response = requests.request("GET", url, headers=headers, data={})
    tempres = response.json()

    res = {}

    for income in tempres['inc_sat']:
        if 'dt' in income:
            income['financial_year'] = income['dt']
            del income['dt']

        if 'ni' in income:
            income['net_income'] = income['ni']
            del income['ni']

        if 'op' in income:
            income['operating_profit'] = income['op']
            del income['op']


    res['standalone_company_imcome_statement_yoy'] = tempres['inc_sat']

    return res


@finRouter.get('/get_stock_consolidated_income_statement')
@finRouter.post('/get_stock_consolidated_income_statement')
async def GetConsolidatedIncomeStatement(request: Request, symbol: str):
    url = f"{DATA_API_HOST}/stocks/fundamental/financial/v1/incomestmt/consolidated?token={master[symbol]}&type=A"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'),
                                         request.headers.get('Authorization'))

    response = requests.request("GET", url, headers=headers, data={})
    tempres = response.json()

    res = {}

    for income in tempres['inc_sat']:
        if 'dt' in income:
            income['financial_year'] = income['dt']
            del income['dt']

        if 'ni' in income:
            income['net_income'] = income['ni']
            del income['ni']

        if 'op' in income:
            income['operating_profit'] = income['op']
            del income['op']

    res['consolidated_company_imcome_statement_yoy'] = tempres['inc_sat']

    return res


@finRouter.get('/get_stock_standalone_valuation')
@finRouter.post('/get_stock_standalone_valuation')
async def GetStandaloneValuation(request: Request, symbol: str):
    url = f"{DATA_API_HOST}/stocks/fundamental/financial/v1/overview/standalone?token={master[symbol]}&type=A"
    headers = add_vensec_auth_to_headers(request.headers.get('session_id'), request.headers.get('x-client-id'),
                                         request.headers.get('Authorization'))

    response = requests.request("GET", url, headers=headers, data={})
    tempres = response.json()

    res = {}

    if 'fv' in tempres:
        res['stock_face_value'] = tempres['fv']
    if 'bv' in tempres:
        res['company_book_value'] = tempres['bv']
    if 'yield' in tempres:
        res['dividend_yield'] = tempres['yield']
    if 'debt_eq' in tempres:
        res['debt_equity_ratio'] = tempres['debt_eq']
    if 'pb' in tempres:
        res['price_book_ratio'] = tempres['pb']

    return res