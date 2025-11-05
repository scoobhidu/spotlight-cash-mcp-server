import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, TRY_LOGIN

overview_mcp = FastMCP(name="Overview MCP")

@overview_mcp.tool(
    name="stock_overview_data_analysis",
    description="Fetch overview summary and returns summary for a given stock symbol.",
)
def stock_overview_data_analysis(
    ctx: Context, symbol: str,
) -> str:
    headers = _build_api_headers(ctx.session_id)
    endpoints = {
        "Overview data available for the stock": f"{API_HOST}/get_stock_overview_summary?symbol={symbol}",
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

        return "\n\n".join(text_blocks)

    except requests.Timeout:
        return f"Error fetching overview data: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error fetching overview data: {exc}\n{TRY_LOGIN}"