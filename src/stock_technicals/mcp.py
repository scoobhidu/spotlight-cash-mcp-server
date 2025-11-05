import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, TRY_LOGIN

technical_mcp = FastMCP(name="Stock Technicals")

@technical_mcp.tool(
    name="stock_technical_data_analysis",
    description="Fetch technical analysis data such as SMA and pivot levels for a given stock symbol.",
)
def stock_technical_data_analysis(
    ctx: Context, symbol: str,
) -> str:
    headers = _build_api_headers(ctx.session_id)
    endpoints = {
        "SMA of different durations for the stock": f"{API_HOST}/get_stock_simple_moving_average?symbol={symbol}",
        "Pivots with support resistance for the stock": f"{API_HOST}/get_stock_pivots?symbol={symbol}",
    }

    try:
        results = {}
        for key, url in endpoints.items():
            resp = requests.get(url, headers=headers, timeout=60)
            resp.raise_for_status()
            results[key] = resp.json()

        text_blocks = []
        for key, data in results.items():
            pretty = json.dumps(data, indent=2, ensure_ascii=False)
            text_blocks.append(f"{key}:\n{pretty}")

        return (
            f"{text_blocks}"
            f"{DISCLAIMER}"
        )

    except requests.Timeout:
        return "Error fetching technical data: request timed out after 60 seconds"
    except requests.RequestException as exc:
        return f"Error fetching technical data: {exc}\n{TRY_LOGIN}"
