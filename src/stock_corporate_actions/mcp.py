import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, TRY_LOGIN

corporate_actions_mcp = FastMCP(name="Corp. Actions MCP")

@corporate_actions_mcp.tool(
    name="stock_corporate_action_analysis",
    description="Fetch corporate actions, dividends, and board announcements for a given stock symbol.",
)
def stock_corporate_action_analysis(
    ctx: Context, symbol: str,
) -> str:
    headers = _build_api_headers(ctx.session_id)
    endpoints = {
        "Recent corporate actions": f"{API_HOST}/get_stock_corporate_actions?symbol={symbol}",
        "Recent dividend announcements": f"{API_HOST}/get_stock_dividends?symbol={symbol}",
        "Latest board announcements of the stock": f"{API_HOST}/get_stock_board_announcements?symbol={symbol}",
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
        return f"Error fetching corporate action data: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error fetching corporate action data: {exc}\n{TRY_LOGIN}"