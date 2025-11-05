import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, TRY_LOGIN

indian_sector_mcp = FastMCP(name="Sector Movement MCP")


@indian_sector_mcp.tool(
    name="indian_sectoral_movement_data_analysis",
    description="Fetch and return Indian indices and sectoral movement data for analysis.",
)
def indian_sectoral_movement_data_analysis(
        ctx: Context,
) -> str:
    headers = _build_api_headers(ctx.session_id)
    endpoints = {
        "Indian indices data": f"{API_HOST}/indian_indices_movement",
        "Indian Sector movement data": f"{API_HOST}/indian_sector_movement",
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
        return f"Error fetching sectoral data: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error fetching sectoral data: {exc}\n{TRY_LOGIN}"



