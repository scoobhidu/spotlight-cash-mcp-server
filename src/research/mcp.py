import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, TRY_LOGIN

research_mcp = FastMCP(name="Equity Marketwatch")


@research_mcp.tool(
    name="new_equity_investment_calls",
    description="Fetch latest equity investment calls given by ventura's spotlight team",
)
def new_equity_investment_calls(
    ctx: Context,
    start_dt: Annotated[str, Field(description="start date from which the research calls have to be fetched, date should be in the format yyyy-mm-dd")],
    end_dt: Annotated[str, Field(description="end date till which the research calls have to be fetched, date should be in the format yyyy-mm-dd")],
    page: Annotated[int, Field(description="its a paginated API, therefore the page number has to be provided. start from 0")],
) -> str:
    url = f"{API_HOST}/research/equities_investment"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, timeout=60, data=json.dumps({
            "start_dt": start_dt,
            "end_dt": end_dt,
            "page": page,
        }))
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        return (
            f"{pretty}"
            f"for any URL that you find for the research document, please list them all as they are probably research docs explaining the company's work and explaination of the research call"
            f"{DISCLAIMER}"
        )
    except requests.Timeout:
        return f"Error fetching open equity research calls: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        # Try to attach any server-provided error details
        extra = ""
        try:
            err_json = response.json() if "response" in locals() and response is not None else None
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}\n{TRY_LOGIN}"
        except Exception:
            pass
        return f"Error fetching open equity research calls: {exc}{extra}\n{TRY_LOGIN}"


@research_mcp.tool(
    name="new_quarterly_results_equity_investment_calls",
    description="Fetch latest equity investment calls given by ventura's spotlight team based on recently announced quarterly results of companies",
)
def new_quarterly_results_equity_investment_calls(
    ctx: Context,
    start_dt: Annotated[str, Field(description="start date from which the research calls have to be fetched, date should be in the format yyyy-mm-dd")],
    end_dt: Annotated[str, Field(description="end date till which the research calls have to be fetched, date should be in the format yyyy-mm-dd")],
    page: Annotated[int, Field(description="its a paginated API, therefore the page number has to be provided. start from 0")],
) -> str:
    url = f"{API_HOST}/research/quarterly_results"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, timeout=60, data=json.dumps({
            "start_dt": start_dt,
            "end_dt": end_dt,
            "page": page,
        }))
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        return (
            f"{pretty}"
            f"for any URL that you find for the research document, please list them all as they are probably research docs explaining the company's work and explaination of the research call"
            f"{DISCLAIMER}"
        )
    except requests.Timeout:
        return f"Error fetching open equity research calls: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        # Try to attach any server-provided error details
        extra = ""
        try:
            err_json = response.json() if "response" in locals() and response is not None else None
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}\n{TRY_LOGIN}"
        except Exception:
            pass
        return f"Error fetching open equity research calls: {exc}{extra}\n{TRY_LOGIN}"


@research_mcp.tool(
    name="new_equity_trading_calls",
    description="Fetch latest equity trading calls given by ventura's spotlight team",
)
def new_equity_trading_calls(
    ctx: Context,
    start_dt: Annotated[str, Field(description="start date from which the research calls have to be fetched, date should be in the format yyyy-mm-dd")],
    end_dt: Annotated[str, Field(description="end date till which the research calls have to be fetched, date should be in the format yyyy-mm-dd")],
    page: Annotated[int, Field(description="its a paginated API, therefore the page number has to be provided. start from 0")],
) -> str:
    url = f"{API_HOST}/research/trading_equities"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, timeout=60, data=json.dumps({
            "start_dt": start_dt,
            "end_dt": end_dt,
            "page": page,
        }))
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        return (
            f"{pretty}"
            f"for any URL that you find for the research document, please list them all as they are probably research docs explaining the company's work and explaination of the research call"
            f"{DISCLAIMER}"
        )
    except requests.Timeout:
        return f"Error fetching open trading research calls: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        # Try to attach any server-provided error details
        extra = ""
        try:
            err_json = response.json() if "response" in locals() and response is not None else None
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}\n{TRY_LOGIN}"
        except Exception:
            pass
        return f"Error fetching open trading research calls: {exc}{extra}\n{TRY_LOGIN}"


@research_mcp.tool(
    name="new_options_trading_calls",
    description="Fetch latest future/option trading calls given by ventura's spotlight team",
)
def new_options_trading_calls(
    ctx: Context,
    start_dt: Annotated[str, Field(description="start date from which the research calls have to be fetched, date should be in the format yyyy-mm-dd")],
    end_dt: Annotated[str, Field(description="end date till which the research calls have to be fetched, date should be in the format yyyy-mm-dd")],
    page: Annotated[int, Field(description="its a paginated API, therefore the page number has to be provided. start from 0")],
) -> str:
    url = f"{API_HOST}/research/trading_options"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, timeout=60, data=json.dumps({
            "start_dt": start_dt,
            "end_dt": end_dt,
            "page": page,
        }))
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        return (
            f"{pretty}"
            f"for any URL that you find for the research document, please list them all as they are probably research docs explaining the company's work and explaination of the research call"
            f"{DISCLAIMER}"
        )
    except requests.Timeout:
        return f"Error fetching open options research calls: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        # Try to attach any server-provided error details
        extra = ""
        try:
            err_json = response.json() if "response" in locals() and response is not None else None
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}\n{TRY_LOGIN}"
        except Exception:
            pass
        return f"Error fetching open options trading research calls: {exc}{extra}\n{TRY_LOGIN}"
