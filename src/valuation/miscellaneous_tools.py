import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER

miscellaneous_mcp = FastMCP(name="Stock Technicals")

@miscellaneous_mcp.tool(
    name="sector_rotation_graph",
    description="Fetch the 1 month or 1 year data of indian sectoral indices and create a [momentum vs relative strength] relative rotation graph to understand leading, lagging, improving and weakening sectors. this will give the user an overview of which sector stocks to buy/sell/hold",
)
def sector_rotation_graph(
    ctx: Context
) -> str:
    return (
        '''
        create a sector relative rotation graph for indian indices after fetching their 1month or 1year graph data
        trace their previous 1 month movements aggregated week-on-week basis on the graph using dotted line
        or if 1 year data is fetched them month-on-month basis on the graph using dotted line.
        
        if you searched the data or any news on the internet make sure to give the user a disclaimer regarding the inaccuracy of data and to do their due diligence before taking any financial decision based on this graph or data. 
        '''
        f"{DISCLAIMER}"
    )


@miscellaneous_mcp.tool(
    name="valuation_dcf",
    description="",
)
def valuation_dcf(
    ctx: Context,
    symbol: str
) -> str:
    return (f'''
        You are a financial valuation expert tasked with calculating the intrinsic value of {symbol}
         Discounted Cash Flow (DCF) Model
Formula:
Intrinsic Value = Σ(FCFt / (1 + WACC)^t) + Terminal Value / (1 + WACC)^n
Where Terminal Value = FCFn × (1 + g) / (WACC - g)
Required Data:

Historical Data (5 years):

Free Cash Flow (FCF) per year
Revenue growth rates
Operating margins
Capital expenditures
Working capital changes


Current Data:

Total debt outstanding
Cash and cash equivalents
Number of shares outstanding
Beta coefficient
Tax rate


Market Data:
Risk-free rate (10-year treasury yield)
Market risk premium (typically 5-7%)
Industry average growth rates


Assumptions to Generate:

FCF growth rate (next 5-10 years)
Terminal growth rate (2-3%)
WACC calculation components 

Note - Make sure to give the user a disclaimer regarding the inaccuracy of data and to do their due diligence before taking any financial decision based on this data.
    '''
    f"{DISCLAIMER}"
    )


@miscellaneous_mcp.tool(
    name="valuation_ddm_gordon_growth_model",
    description="",
)
def valuation_ddm_gordon_growth_model(
    ctx: Context,
    symbol: str
) -> str:
    return (f'''
        You are a financial valuation expert tasked with calculating the intrinsic value of {symbol}
         Dividend Discount Model (DDM) - Gordon Growth Model
Formula:
Intrinsic Value = D1 / (r - g)
Where: D1 = Expected dividend next year, r = Required rate of return, g = Growth rate
Required Data:

Historical Data (5 years):

Dividend per share history
Dividend growth rate
Payout ratio trends


Current Data:

Current dividend per share
Earnings per share (EPS)
Return on Equity (ROE)
Retention ratio (1 - Payout ratio)


Market Data:

Beta coefficient
Risk-free rate
Market risk premium

Note - Make sure to give the user a disclaimer regarding the inaccuracy of data and to do their due diligence before taking any financial decision based on this data.
    '''
            f"{DISCLAIMER}"
            )


@miscellaneous_mcp.tool(
    name="valuation_garp",
    description="",
)
def valuation_garp(
    ctx: Context,
    symbol: str
) -> str:
    return (f'''
        You are a financial valuation expert tasked with calculating the intrinsic value of {symbol}

GARP (Growth at Reasonable Price) Valuation
Formula:
GARP Fair Value = EPS × (Growth Rate × Quality Factor)
Where Quality Factor = √(ROE × (1 - Payout Ratio) × Earnings Stability)

Adjusted GARP Value = Current EPS × PEG-Adjusted Multiple
PEG-Adjusted Multiple = Growth Rate / PEG Target (typically 1.0-1.5 for GARP)
Alternative GARP Formula (Lynch Method):
Fair P/E = Growth Rate (if PEG = 1)
Intrinsic Value = EPS × Growth Rate × GARP Discount Factor
GARP Discount Factor = 0.5 to 1.0 based on quality metrics
Required Data:

Growth Metrics:

Historical earnings growth (3-5 years)
Projected earnings growth (3-5 years)
Revenue growth rate
Free cash flow growth rate
Analyst consensus growth estimates


Quality Metrics:

Return on Equity (ROE) - last 5 years average
Return on Assets (ROA)
Return on Invested Capital (ROIC)
Debt-to-Equity ratio
Interest coverage ratio
Earnings stability (standard deviation of earnings growth)


Valuation Metrics:

Current P/E ratio
Current PEG ratio
Forward P/E ratio
Price-to-Free Cash Flow ratio


Profitability Metrics:

Operating margin trends
Net profit margin
Gross margin stability
Cash conversion cycle



GARP Scoring Criteria:

Growth Rate: 15-25% (ideal range)
PEG Ratio: < 1.5 (preferably < 1.0)
ROE: > 15%
Debt/Equity: < 0.5
Earnings Quality Score: Based on accruals and cash flow correlation

Note - Make sure to give the user a disclaimer regarding the inaccuracy of data and to do their due diligence before taking any financial decision based on this data.
    '''
            f"{DISCLAIMER}"
            )


@miscellaneous_mcp.tool(
    name="valuation_peg",
    description="",
)
def valuation_peg(
    ctx: Context,
    symbol: str
) -> str:
    return (f'''
        You are a financial valuation expert tasked with calculating the intrinsic value of {symbol}

PEG Ratio Valuation
Formula:
Fair P/E = PEG × Growth Rate
Intrinsic Value = EPS × (PEG × Growth Rate)
Standard PEG = 1.0 for fairly valued stocks

Required Data:

    Company Data:
        Current EPS
        Expected EPS growth rate (3-5 years)
        Current P/E ratio
    
    
    Industry Data:
        Industry average PEG ratio
        Peer group PEG ratios

Note - Make sure to give the user a disclaimer regarding the inaccuracy of data and to do their due diligence before taking any financial decision based on this data.
    '''
            f"{DISCLAIMER}"
            )


@miscellaneous_mcp.tool(
    name="valuation_residual_income_model",
    description="",
)
def valuation_peg(
    ctx: Context,
    symbol: str
) -> str:
    return (f'''
        You are a financial valuation expert tasked with calculating the intrinsic value of {symbol}

Residual Income Model
Formula:
Intrinsic Value = Book Value + Σ(Residual Income_t / (1 + r)^t)
Where Residual Income = Net Income - (Equity × Cost of Equity)
Required Data:

Company Data:
    Book value per share
    Projected net income (5-10 years)
    ROE projections
    Equity capital


Market Data:
    Cost of equity (CAPM)
    Terminal value assumptions

Note - Make sure to give the user a disclaimer regarding the inaccuracy of data as it is generated by AI and to do their due diligence before taking any financial decision based on this data.
    '''
    f"{DISCLAIMER}"
    )