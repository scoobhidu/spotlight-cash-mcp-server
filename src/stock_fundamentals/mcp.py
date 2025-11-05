import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, TRY_LOGIN

fundamental_mcp = FastMCP(name="Fundamental MCP")

@fundamental_mcp.tool(
    name="stock_fundamental_data_analysis",
    description="Fetch and return fundamental data available for a given stock symbol.",
)
def stock_fundamental_data_analysis(
    ctx: Context, symbol: str,
) -> str:
    url = f"{API_HOST}/get_stock_fundamental_data?symbol={symbol}"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)

        return (
            f"Fundamental data available for the stock:\n{pretty}"
            f"{DISCLAIMER}"
        )
    except requests.Timeout:
        return f"Error fetching fundamental data: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        # Try to include any error details the server provided
        extra = ""
        try:
            err_json = response.json()
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}\n{TRY_LOGIN}"
        except Exception:
            pass
        return f"Error fetching fundamental data: {exc}{extra}\n{TRY_LOGIN}"