import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, TRY_LOGIN

global_indices_mcp = FastMCP(name="Global Indices MCP")


@global_indices_mcp.tool(
    name="global_indices_movement",
    description="Fetch all the price changes for global market indices",
)
def get_global_indices_movement(
    ctx: Context,
) -> str:
    url = f"{API_HOST}/global_indices_movement"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        return (
            f"{pretty}"
            f"\n{DISCLAIMER}"
        )
    except requests.Timeout:
        return f"Error fetching global indices data: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        # Try to attach any server-provided error details
        extra = ""
        try:
            err_json = response.json() if "response" in locals() and response is not None else None
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}\n{TRY_LOGIN}"
        except Exception:
            pass
        return f"Error fetching global indices data: {exc}{extra}\n{TRY_LOGIN}"


@global_indices_mcp.tool(
    name="indian_indices_movement",
    description="Fetch all the price changes for global market indices",
)
def get_indian_indices_movement(
    ctx: Context,
) -> str:
    url = f"{API_HOST}/indian_indices_movement"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        return (
            f"{pretty}"
            f"\n{DISCLAIMER}"
        )
    except requests.Timeout:
        return "Error fetching indian indices data: request timed out after 60 seconds"
    except requests.RequestException as exc:
        # Try to attach any server-provided error details
        extra = ""
        try:
            err_json = response.json() if "response" in locals() and response is not None else None
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}"
        except Exception:
            pass
        return f"Error fetching indian indices data: {exc}{extra}\n{TRY_LOGIN}"


@global_indices_mcp.tool(
    name="india_vix",
    description="Fetch the latest updates in India VIX data",
)
def get_indian_vix_updates(
    ctx: Context,
) -> str:
    url = f"{API_HOST}/india_vix_movement"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        return (
            f"{pretty}"
            f"\n{DISCLAIMER}"
        )
    except requests.Timeout:
        return f"Error fetching India VIX data: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        # Try to attach any server-provided error details
        extra = ""
        try:
            err_json = response.json() if "response" in locals() and response is not None else None
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}\n{TRY_LOGIN}"
        except Exception:
            pass
        return f"Error fetching indian vix data: {exc}{extra}\n{TRY_LOGIN}"


@global_indices_mcp.tool(
    name="global_cues_and_indian_indices_movement_analysis",
    description="Fetch and return global cues, Indian indices, VIX, sector movements, and latest news data for analysis.",
)
def global_cues_and_indian_indices_movement_analysis(ctx: Context) -> str:
    return "get the latest updates in global cues, Indian indices, India VIX, sector movements, and latest news data for analysis."

