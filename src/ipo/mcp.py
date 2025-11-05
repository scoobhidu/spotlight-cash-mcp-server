import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, TRY_LOGIN

ipo_mcp = FastMCP(name="IPO Service")


@ipo_mcp.tool(
    name="get_open_ipos",
    description="Fetch all open IPOs in indian markets",
)
def get_open_ipos(
    ctx: Context,
) -> str:
    url = f"{API_HOST}/ipo/ongoing"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        return (f"{pretty}, get the GMP (Gray market trend) for all IPOs and show the user which IPO is a good option for applying"
                f"\n{DISCLAIMER}"
                f"if the response contains a document url, list them all as they are probably research docs explaining the IPO company's work")
    except requests.Timeout:
        return f"Error fetching open IPOs: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        # Try to attach any server-provided error details
        extra = ""
        try:
            err_json = response.json() if "response" in locals() and response is not None else None
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}\n{TRY_LOGIN}"
        except Exception:
            pass
        return f"Error fetching open IPOs: {exc}{extra}\n{TRY_LOGIN}"


@ipo_mcp.tool(
    name="get_closed_ipos",
    description="Fetch all closed IPOs that are about to be listed in indian markets",
)
def get_closed_ipos(
    ctx: Context,
    ipo_code: Annotated[str, Field(description="IPO code")],
) -> str:
    url = f"{API_HOST}/ipo/closed"
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
        return (
            "Error fetching closed IPOs: request timed out after 60 seconds"
            f"\n{TRY_LOGIN}"
        )
    except requests.RequestException as exc:
        # Try to attach any server-provided error details
        extra = ""
        try:
            err_json = response.json() if "response" in locals() and response is not None else None
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}\n{TRY_LOGIN}"
        except Exception:
            pass
        return f"Error fetching closed IPOs: {exc}{extra}\n{TRY_LOGIN}"


@ipo_mcp.tool(
    name="get_listed_ipos",
    description="Fetch all recently listed IPOs in indian markets",
)
def get_listed_ipos(
    ctx: Context,
    ipo_code: Annotated[str, Field(description="IPO code")],
) -> str:
    url = f"{API_HOST}/ipo/listed"
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
        return (
            "Error fetching listed IPOs: request timed out after 60 seconds"
            f"\n{TRY_LOGIN}"
        )
    except requests.RequestException as exc:
        # Try to attach any server-provided error details
        extra = ""
        try:
            err_json = response.json() if "response" in locals() and response is not None else None
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}\n{TRY_LOGIN}"
        except Exception:
            pass
        return f"Error fetching listed IPOs: {exc}{extra}\n{TRY_LOGIN}\n{TRY_LOGIN}"


@ipo_mcp.tool(
    name="get_ipo_details",
    description="Fetch details of a given IPO - returns only the ",
)
def get_ipo_details(
    ctx: Context,
    ipo_code: Annotated[str, Field(description="IPO code")],
) -> str:
    url = f"{API_HOST}/ipo/details?ipo_code={ipo_code}"
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
        return f"Error fetching open IPOs: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        # Try to attach any server-provided error details
        extra = ""
        try:
            err_json = response.json() if "response" in locals() and response is not None else None
            if err_json:
                extra = f" - {json.dumps(err_json, ensure_ascii=False)}\n{TRY_LOGIN}"
        except Exception:
            pass
        return f"Error fetching open IPOs: {exc}{extra}\n{TRY_LOGIN}"

