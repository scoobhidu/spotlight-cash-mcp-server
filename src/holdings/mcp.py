import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, TRY_LOGIN

holdings_mcp = FastMCP(name="FnO Marketwatch")

@holdings_mcp.tool(
    name="complete_portfolio_with_data_of_holdings",
    description="Fetch complete portfolio and return a text block for analysis using only the provided holdings data.",
)
def completely_detailed_portfolio_with_data_of_holdings_analysis(
    ctx: Context,
) -> str:
    url = f"{API_HOST}/fetch_complete_portfolio"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        return (
            "You are supposed to provide analysis based on the list of holdings given below only. If there's no holding in the given data then tell the same to the user."
            f"Current Holdings Data:\n{pretty}"
            f"\n{DISCLAIMER}"
        )
    except requests.Timeout:
        return f"Error fetching portfolio: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        # Try to attach any server-provided error details
        extra = ""
        try:
            err_json = response.json() if "response" in locals() and response is not None else None
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}\n{TRY_LOGIN}"
        except Exception:
            pass
        return f"Error fetching portfolio: {exc}{extra}\n{TRY_LOGIN}"