import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, TRY_LOGIN

financial_mcp = FastMCP(name="Financial MCP")


@financial_mcp.tool(
    name="stock_financials_summary",
    description="Fetch financial summaries for a given stock symbol.",
)
def stock_financial_and_results_analysis(
    ctx: Context, symbol: str,
) -> str:
    headers = _build_api_headers(ctx.session_id)
    endpoints = {
        "Financial data available for the stock": f"{API_HOST}/get_stock_financial_summary?symbol={symbol}",
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
        return f"Error fetching financial summary data: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error fetching financial summary data: {exc}\n{TRY_LOGIN}"



@financial_mcp.tool(
    name="stock_standalone_income_statement",
    description="Fetch standalone income statements for a given stock symbol.",
)
def stock_financial_and_results_analysis(
    ctx: Context, symbol: str,
) -> str:
    headers = _build_api_headers(ctx.session_id)
    endpoints = {
        "Standalone income statement of the stock": f"{API_HOST}/get_stock_standalone_income_statement?symbol={symbol}",
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
        return f"Error fetching standalone income data: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error fetching standalone income data: {exc}\n{TRY_LOGIN}"



@financial_mcp.tool(
    name="stock_consolidated_income_statement",
    description="Fetch consolidated income statements for a given stock symbol.",
)
def stock_financial_and_results_analysis(
    ctx: Context, symbol: str,
) -> str:
    headers = _build_api_headers(ctx.session_id)
    endpoints = {
        "Consolidated income statements of the stock": f"{API_HOST}/get_stock_consolidated_income_statement?symbol={symbol}",
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
        return f"Error fetching consolidated income data: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error fetching consolidated income data: {exc}\n{TRY_LOGIN}"



@financial_mcp.tool(
    name="stock_valuation_summary_data",
    description="Fetch valuations summary for a given stock symbol.",
)
def stock_valuation_summary_data(
    ctx: Context, symbol: str,
) -> str:
    headers = _build_api_headers(ctx.session_id)
    endpoints = {
        "Standalone valuations of the stock": f"{API_HOST}/get_stock_standalone_valuation?symbol={symbol}",
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
        return f"Error fetching valuation summary data: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error fetching valuation summary data: {exc}\n{TRY_LOGIN}"

