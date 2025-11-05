import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, TRY_LOGIN

fno_mktwatch_mcp = FastMCP(name="FnO Marketwatch")


@fno_mktwatch_mcp.tool(
    name="stock_future_movers_today",
    description="Paginated tool to get the stock futures in Nifty 500 that were the top OI gainer or losers or the top Price gainer or losers for the day",
)
def stock_fut_movers_today(
    ctx: Context,
    type_filter: Annotated[Literal["oigainer", "oiloser", "pricegainer", "priceloser"], Field(description="identifier to get stock futures that were the top OI gainer or losers or the top Price gainer or losers for the day")],
    page: Annotated[int, Field(description="page number to get stocks near high or low of specified duration because this is a paginated tool, increase the number only to get more stocks if any")] = 0,
    tag: Annotated[Literal['W1', 'W2', 'W3', 'W4', 'M1', 'M2', 'M3'], Field(description="only nifty and sensex are weekly rest all are monthly expiring contracts, Weekly is according to the week of the month. Use M1 for stocks near current month end expiry, M2 for next month expiry and M3 accordingly")] = "M1",
) -> str:
    url = f"{API_HOST}/futuremovers/stocks/{type_filter}?page={page}"

    headers = _build_api_headers(ctx.session_id)
    try:
        resp = requests.post(url, headers=headers, timeout=30, data=json.dumps({
            "expiry_type": tag,
        }))
        resp.raise_for_status()
        return (
            f"{type_filter} stock futures:\n{json.dumps(resp.json(), indent=2, ensure_ascii=False)}"
            f"\n{DISCLAIMER}"
        )
    except requests.RequestException as exc:
        return f"Error fetching the selected filter: {exc}\n{TRY_LOGIN}"


@fno_mktwatch_mcp.tool(
    name="indices_future_movers_today",
    description="Paginated tool to get the indices that were the top OI gainer or losers or the top Price gainer or losers for the day",
)
def index_fut_movers_today(
    ctx: Context,
    type_filter: Annotated[Literal["oigainer", "oiloser", "pricegainer", "priceloser"], Field(description="identifier to get the indices that were the top OI gainer or losers or the top Price gainer or losers for the day")],
    page: Annotated[int, Field(description="page number to get indices near high or low of specified duration because this is a paginated tool, increase the number only to get more indices if any")] = 0,
    tag: Annotated[Literal['W1', 'W2', 'W3', 'W4', 'M1', 'M2', 'M3'], Field(description="only nifty and sensex are weekly rest all are monthly expiring contracts, Weekly is according to the week of the month. Use M1 for stocks near current month end expiry, M2 for next month expiry and M3 accordingly")] = "M1",
) -> str:
    url = f"{API_HOST}/futuremovers/indices/{type_filter}?page={page}"

    headers = _build_api_headers(ctx.session_id)
    try:
        resp = requests.post(url, headers=headers, timeout=30, data=json.dumps({
            "expiry_type": tag,
        }))
        resp.raise_for_status()
        return (
            f"{type_filter} indices futures:\n{json.dumps(resp.json(), indent=2, ensure_ascii=False)}"
            f"\n{DISCLAIMER}"
        )
    except requests.RequestException as exc:
        return f"Error fetching the selected filter: {exc}\n{TRY_LOGIN}"



@fno_mktwatch_mcp.tool(
    name="stock_options_movers_today",
    description="Paginated tool to get the stock options in Nifty 500 that were the top OI gainer or losers or the top Price gainer or losers or active by volume for the day",
)
def stock_fut_movers_today(
    ctx: Context,
    type_filter: Annotated[Literal["oigainer", "oiloser", "pricegainer", "priceloser", "activevol"], Field(description="identifier to get stock options that were the top OI gainer or losers or the top Price gainer or losers or the most active by volume for the day")],
    page: Annotated[int, Field(description="page number to get options near high or low of specified duration because this is a paginated tool, increase the number only to get more options if any")] = 0,
    tag: Annotated[Literal['W1', 'W2', 'W3', 'W4', 'M1', 'M2', 'M3'], Field(description="only nifty and sensex are weekly rest all are monthly expiring contracts, Weekly is according to the week of the month. Use M1 for stocks near current month end expiry, M2 for next month expiry and M3 accordingly")] = "M1",
) -> str:

    url = f"{API_HOST}/optmovers/stocks/{type_filter}?page={page}"

    headers = _build_api_headers(ctx.session_id)
    try:
        resp = requests.post(url, headers=headers, timeout=30, data=json.dumps({
            "expiry_type": tag,
        }))
        resp.raise_for_status()
        return (
            f"{type_filter} stock options:\n{json.dumps(resp.json(), indent=2, ensure_ascii=False)}"
            f"\n{DISCLAIMER}"
        )
    except requests.RequestException as exc:
        return f"Error fetching the selected filter: {exc}\n{TRY_LOGIN}"


@fno_mktwatch_mcp.tool(
    name="index_options_movers_today",
    description="Paginated tool to get the index options in Nifty 500 that were the top OI gainer or losers or the top Price gainer or losers or active by volume for the day",
)
def stock_fut_movers_today(
    ctx: Context,
    type_filter: Annotated[Literal["oigainer", "oiloser", "pricegainer", "priceloser", "activevol"], Field(description="identifier to get stock options that were the top OI gainer or losers or the top Price gainer or losers or the most active by volume for the day")],
    page: Annotated[int, Field(description="page number to get options near high or low of specified duration because this is a paginated tool, increase the number only to get more options if any")] = 0,
    tag: Annotated[Literal['W1', 'W2', 'W3', 'W4', 'M1', 'M2', 'M3'], Field(description="only nifty and sensex are weekly rest all are monthly expiring contracts, Weekly is according to the week of the month. Use M1 for stocks near current month end expiry, M2 for next month expiry and M3 accordingly")] = "M1",
) -> str:
    url = f"{API_HOST}/optmovers/indices/{type_filter}?page={page}"

    headers = _build_api_headers(ctx.session_id)
    try:
        resp = requests.post(url, headers=headers, timeout=30, data=json.dumps({
            "expiry_type": tag,
        }))
        resp.raise_for_status()
        return (
            f"{type_filter} index options:\n{json.dumps(resp.json(), indent=2, ensure_ascii=False)}"
            f"\n{DISCLAIMER}"
        )
    except requests.RequestException as exc:
        return f"Error fetching the selected filter: {exc}\n{TRY_LOGIN}"


@fno_mktwatch_mcp.tool(
    name="stock_future_oi_analysis",
    description="Paginated tool to get the stock futures currently in Long Buildup, Short Buildup, Long Unwinding and Short Covering",
)
def stock_future_oi_analysis(
    ctx: Context,
    buildup_type: Annotated[Literal["LB", "SB", "LU", "SC"], Field(description="identifier to find stock futures currently in Long Buildup, Short Buildup, Long Unwinding and Short Covering")],
    page: Annotated[int, Field(description="page number because this is a paginated tool, increase the number only to get more stock futures if any")] = 0,
) -> str:
    url = f"{API_HOST}/futuremovers/stocks/oianalysis?page={page}"
    headers = _build_api_headers(ctx.session_id)
    try:
        resp = requests.post(url, headers=headers, timeout=30, data=json.dumps({
            "type": buildup_type
        }))
        resp.raise_for_status()
        return (
            f"{buildup_type} Stock Futures: \n{json.dumps(resp.json(), indent=2, ensure_ascii=False)}"
            f"\n{DISCLAIMER}"
        )
    except requests.RequestException as exc:
        return f"Error fetching the stock futures: {exc}\n{TRY_LOGIN}"



@fno_mktwatch_mcp.tool(
    name="indices_future_oi_analysis",
    description="Paginated tool to get the index futures currently in Long Buildup, Short Buildup, Long Unwinding and Short Covering",
)
def index_future_oi_analysis(
    ctx: Context,
    buildup_type: Annotated[Literal["LB", "SB", "LU", "SC"], Field(description="identifier to find index futures currently in Long Buildup, Short Buildup, Long Unwinding and Short Covering")],
    page: Annotated[int, Field(description="page number because this is a paginated tool, increase the number only to get more index futures if any")] = 0,
) -> str:
    url = f"{API_HOST}/futuremovers/indices/oianalysis?page={page}"
    headers = _build_api_headers(ctx.session_id)
    try:
        resp = requests.post(url, headers=headers, timeout=30, data=json.dumps({
        "type": buildup_type
    }))
        resp.raise_for_status()
        return (
            f"{buildup_type} Index Futures: \n{json.dumps(resp.json(), indent=2, ensure_ascii=False)}"
            f"\n{DISCLAIMER}"
        )
    except requests.RequestException as exc:
        return f"Error fetching the index futures: {exc}\n{TRY_LOGIN}"


@fno_mktwatch_mcp.tool(
    name="stocks_with_fut_and_options",
    description="Fetch all listed stocks that have derivative contracts (futures and options) and return as a text block.",
)
def stocks_with_fut_and_options(
    ctx: Context,
) -> str:
    url = f"{API_HOST}/all_stocks_futures"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        return (
            "All listed stocks with derivative contracts:\n"
            f"{pretty}"
            f"\n{DISCLAIMER}"
        )
    except requests.Timeout:
        return "Error fetching stocks data: request timed out after 60 seconds"
    except requests.RequestException as exc:
        # Try to attach any server-provided error details
        extra = ""
        try:
            err_json = response.json() if "response" in locals() and response is not None else None
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}"
        except Exception:
            pass
        return f"Error fetching stocks data: {exc}{extra}\n{TRY_LOGIN}"

