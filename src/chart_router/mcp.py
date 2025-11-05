import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, TRY_LOGIN

charts_mcp = FastMCP(name="Charts MCP")



@charts_mcp.tool(
    name="nse_stock_line_chart",
    description="Fetch and return NSE line chart data for a given stock symbol and given time period.",
)
def nse_stock_line_chart(
    ctx: Context, symbol: str, time_period: Annotated[
        Literal["1d", "1w", "1m", "1y", "3y", "5y", "all"],
        Field(description="Time period over which the line-chart data has to be given")
    ] = "1d"
) -> str:
    url = f"{API_HOST}/nse_line_chart?symbol={symbol}&period={time_period}"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)

        return (
            f"NSE line chart data for {symbol}:\n{pretty}"
            f"\n{DISCLAIMER}"
        )
    except requests.Timeout:
        return f"Error fetching NSE line chart: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        # Try to include any server-provided error details
        extra = ""
        try:
            err_json = response.json()
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}\n{TRY_LOGIN}"
        except Exception:
            pass
        return f"Error fetching NSE line chart: {exc}{extra}\n{TRY_LOGIN}"


@charts_mcp.tool(
    name="bse_stock_line_chart",
    description="Fetch and return BSE line chart data for a given stock symbol and given time period.",
)
def bse_stock_line_chart(
    ctx: Context, symbol: str, time_period: Annotated[
        Literal["1d", "1w", "1m", "1y", "3y", "5y", "all"],
        Field(description="Time period over which the line-chart data has to be given")
    ] = "1d"
) -> str:
    url = f"{API_HOST}/bse_line_chart?symbol={symbol}&period={time_period}"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)

        return (
            f"BSE line chart data for {symbol}:\n{pretty}"
            f"\n{DISCLAIMER}"
        )
    except requests.Timeout:
        return f"Error fetching BSE line chart: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        # Try to include any server-provided error details
        extra = ""
        try:
            err_json = response.json()
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}"
        except Exception:
            pass
        return f"Error fetching BSE line chart: {exc}{extra}\n{TRY_LOGIN}"


@charts_mcp.tool(
    name="index_line_chart",
    description="Fetch and return line chart data for a given indian index symbol and given time period.",
)
def index_stock_line_chart(
    ctx: Context, symbol: str, time_period: Annotated[
        Literal["1d", "1w", "1m", "1y", "3y", "5y", "all"],
        Field(description="Time period over which the line-chart data has to be given")
    ] = "1d"
) -> str:
    url = f"{API_HOST}/index_line_chart?symbol={symbol}&period={time_period}"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)

        return (
            f"Index line chart data for {symbol}:\n{pretty}"
            f"\n{DISCLAIMER}"
        )
    except requests.Timeout:
        return f"Error fetching Index line chart: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        # Try to include any server-provided error details
        extra = ""
        try:
            err_json = response.json()
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}\n{TRY_LOGIN}"
        except Exception:
            pass
        return f"Error fetching Index line chart: {exc}{extra}\n{TRY_LOGIN}"


@charts_mcp.tool(
    name="future_or_options_line_chart",
    description="Fetch and return line chart data for a given future or option symbol and given time period.",
)
def fno_stock_line_chart(
    ctx: Context, symbol: str, time_period: Annotated[
        Literal["1d", "1w", "1m"],
        Field(description="Time period over which the line-chart data has to be given")
    ] = "1d"
) -> str:
    url = f"{API_HOST}/nfo_line_chart?symbol={symbol}&period={time_period}"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)

        return (
            f"FnO line chart data for {symbol}:\n{pretty}"
            f"\n{DISCLAIMER}"
        )
    except requests.Timeout:
        return f"Error fetching FnO line chart: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        # Try to include any server-provided error details
        extra = ""
        try:
            err_json = response.json()
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}\n{TRY_LOGIN}"
        except Exception:
            pass
        return f"Error fetching FnO line chart: {exc}{extra}\n{TRY_LOGIN}"

