import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, DISCLAIMER, TRY_LOGIN

options_mcp = FastMCP(name="Options MCP")

@options_mcp.tool(
    name="stock_option_chain_analysis",
    description="Fetch stock option chain data for a given stock symbol.",
)
def stock_option_chain_analysis(
    ctx: Context, symbol: str,
) -> str:
    headers = _build_api_headers(ctx.session_id)
    endpoints = {
        "Stock option chain data": f"{API_HOST}/get_complete_stock_option_chain_data?symbol={symbol}",
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
            f"\n{text_blocks}"
            f"\n{DISCLAIMER}"
        )

    except requests.Timeout:
        return f"Error fetching option chain data: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error fetching option chain data: {exc}\n{TRY_LOGIN}"


@options_mcp.tool(
    name="stock_oi_pcr_data_analysis",
    description="Fetch future/option Open-interest and put-call-ratio data for a given stock symbol.",
)
def stock_oi_pcr_data_analysis(
    ctx: Context, symbol: str,
) -> str:
    headers = _build_api_headers(ctx.session_id)
    endpoints = {
        "Stock all expiration OI PCR for the day data": f"{API_HOST}/get_oi_pcr_data?symbol={symbol}",
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
            f"\n{DISCLAIMER}"
        )

    except requests.Timeout:
        return f"Error fetching OI PCR data: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error fetching OI PCR data: {exc}\n{TRY_LOGIN}"


@options_mcp.tool(
    name="stock_future_oi_timeseries_analysis",
    description="Fetch futures OI timeseries data for a given stock symbol.",
)
def stock_future_oi_timeseries_analysis(
    ctx: Context, symbol: str,
) -> str:
    headers = _build_api_headers(ctx.session_id)
    endpoints = {
        "Stock all expiration series future OI timeseries for the day data": f"{API_HOST}/get_fut_oi_timeseries_data?symbol={symbol}",
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
            f"\n{DISCLAIMER}"
        )

    except requests.Timeout:
        return f"Error fetching future's OI timeseries data: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error fetching future's OI timeseries data: {exc}\n{TRY_LOGIN}"


@options_mcp.tool(
    name="strategy_builder",
    description="Prepare an options trading strategy for a given symbol using market cues, option chain, news, charts, fundamentals, and technicals.",
)
def strategy_builder(
    symbol: Annotated[str, Field(description="Symbol of the instrument to analyse and prepare a strategy for. Leave empty for general strategy building.")] = "",
) -> str:
    try:
        # This tool doesn’t fetch from API — it returns structured strategy guidance
        return (
            f"""
You are an excellent trader and are supposed to prepare a strategy with a high probability 
of success in the underlying instrument {symbol if symbol else "[no symbol provided]"}.

Follow the global and Indian market cues. Analyse any sectoral implications.
Carefully analyse the option chain of the underlying instrument. Look into the latest news (both stock-specific and global).
Do a 1-day, 1-week, and 1-month chart analysis. Take note of fundamentals and technicals.

The strategy should be option Greeks–optimised for Indian markets, focusing on:
- Delta targeting (0.15–0.35 for selling strategies, delta-neutral within ±0.05)
- Gamma exposure management around weekly expiry schedules
- Theta harvesting (0.02%–0.05% daily collection, focus 30–7 DTE)
- Vega optimisation based on India VIX (rank >75% for selling, <25% for buying)
- Rho negligible except for LEAPS
- POP, Monte Carlo simulation, Sharpe ratio >1.5

Risk management:
- Limit max 1-day stressed loss to 2% of portfolio, 1-week stressed loss to 5%
- System alerts for Delta ±40%, Gamma >0.04, Vega >1.5%, Theta <0.01%

Suggested strategies (adjust to conditions): Covered Call, Protective Put, Cash Secured Put, Bull Call Spread, Bear Put Spread, Iron Condor, Ratio Backspreads, Jade Lizard, Broken Wing strategies, Double Diagonal, Long Combo, Synthetic Futures, Straddles/Strangles

Use sectoral context, news, and technicals to adapt which of these fits best.
            """
        )

    except Exception as exc:
        return f"Error building strategy: {str(exc)}\n{TRY_LOGIN}"