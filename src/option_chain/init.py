import requests
from fastapi import APIRouter, Request

from headers_util import add_niftytrader_auth_to_headers

ocRouter = APIRouter()

class OptionChain:
    def __init__(self, niftytraderauth):
        self.niftytraderauth = niftytraderauth

    async def GetCompleteOptionChainData(self, res):
        for h in res['user_portfolio']['holdings']:
            if res['user_portfolio']['holdings'][h]['has_future_contract']:
                url = f"https://webapi.niftytrader.in/webapi/option/option-chain-data?symbol={res['user_portfolio']['holdings'][h]['sym']}&exchange=nse&expiryDate=&atmBelow=10&atmAbove=10"
                headers = add_niftytrader_auth_to_headers(self.niftytraderauth)

                response = requests.request("GET", url, headers=headers, data={})

                tempres = response.json()

                res['user_portfolio']['holdings'][h]['option_chain_details'] = tempres['resultData']['opDatas']

                tempres['resultData']['opTotals']['in_the_money_total_calls'] = tempres['resultData']['opTotals']['itm_total_calls']
                tempres['resultData']['opTotals']['in_the_money_total_puts'] = tempres['resultData']['opTotals']['itm_total_puts']
                tempres['resultData']['opTotals']['out_of_the_money_total_calls'] = tempres['resultData']['opTotals']['otm_total_calls']
                tempres['resultData']['opTotals']['out_of_the_money_total_puts'] = tempres['resultData']['opTotals']['otm_total_puts']

                tempres['resultData']['opTotals']['total_calls_puts_summary'] = tempres['resultData']['opTotals']['total_calls_puts']

                del tempres['resultData']['opTotals']['itm_total_calls']
                del tempres['resultData']['opTotals']['itm_total_puts']
                del tempres['resultData']['opTotals']['otm_total_calls']
                del tempres['resultData']['opTotals']['otm_total_puts']
                del tempres['resultData']['opTotals']['total_calls_puts']

                res['user_portfolio']['holdings'][h]['option_chain_summary'] = tempres['resultData']['opTotals']


@ocRouter.get('/get_complete_stock_option_chain_data')
@ocRouter.post('/get_complete_stock_option_chain_data')
async def GetCompleteOptionChainData(request: Request, symbol: str):
    url = f"https://webapi.niftytrader.in/webapi/option/option-chain-data?symbol={symbol}&exchange=nse&expiryDate=&atmBelow=10&atmAbove=10"
    headers = add_niftytrader_auth_to_headers(request.headers.get('niftytraderauth'))

    response = requests.request("GET", url, headers=headers, data={})

    tempres = response.json()

    res = {'option_chain_details': tempres['resultData']['opDatas']}

    tempres['resultData']['opTotals']['in_the_money_total_calls'] = tempres['resultData']['opTotals']['itm_total_calls']
    tempres['resultData']['opTotals']['in_the_money_total_puts'] = tempres['resultData']['opTotals']['itm_total_puts']
    tempres['resultData']['opTotals']['out_of_the_money_total_calls'] = tempres['resultData']['opTotals']['otm_total_calls']
    tempres['resultData']['opTotals']['out_of_the_money_total_puts'] = tempres['resultData']['opTotals']['otm_total_puts']

    tempres['resultData']['opTotals']['total_calls_puts_summary'] = tempres['resultData']['opTotals']['total_calls_puts']

    del tempres['resultData']['opTotals']['itm_total_calls']
    del tempres['resultData']['opTotals']['itm_total_puts']
    del tempres['resultData']['opTotals']['otm_total_calls']
    del tempres['resultData']['opTotals']['otm_total_puts']
    del tempres['resultData']['opTotals']['total_calls_puts']

    res['option_chain_summary'] = tempres['resultData']['opTotals']

    return res
