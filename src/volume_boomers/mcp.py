import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, TRY_LOGIN

volume_boomers_mcp = FastMCP(name="Volume Boomers")


@volume_boomers_mcp.tool(
    name="get_stock_volume_boomers",
    description="Fetch all stocks that have had an increase in the traded volume creating an opportunity of buy or sell",
)
def get_stock_volume_boomers(
    ctx: Context,
) -> str:
    url = f"{API_HOST}/get_stock_volume_boomers"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        return (
            f"{pretty}"
            f"{DISCLAIMER}"
        )

    except requests.Timeout:
        return "Error fetching volume boomers: request timed out after 60 seconds"
    except requests.RequestException as exc:
        # Try to attach any server-provided error details
        extra = ""
        try:
            err_json = response.json() if "response" in locals() and response is not None else None
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}"
        except Exception:
            pass
        return f"Error fetching volume boomers: {exc}{extra}\n{TRY_LOGIN}"

