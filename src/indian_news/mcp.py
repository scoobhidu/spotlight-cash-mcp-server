import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, TRY_LOGIN

news_mcp = FastMCP(name="News MCP")

@news_mcp.tool(
    name="latest_news_summary_analysis",
    description="Fetch and return the latest Indian & Global news summaries. Optionally fetch stock-specific news when a symbol is provided.",
)
def latest_news_summary_analysis(
        ctx: Context, symbol: str | None = None
) -> str:
    headers = _build_api_headers(ctx.session_id)
    urls = [
        f"{API_HOST}/get_20_latest_news_summary",
    ]
    if symbol:
        urls.append(f"{API_HOST}/get_10_latest_stock_news_summary?symbol={symbol}")

    try:
        results = []
        for url in urls:
            resp = requests.get(url, headers=headers, timeout=60)
            resp.raise_for_status()
            results.append(resp.json())

        # Always include global news
        output = [
            "Crawl the links in the data to understand Indian & Global News data:\n"
            f"{json.dumps(results[0], indent=2, ensure_ascii=False)}\n\n"
            "If not enough to understand try searching by yourself as well"
            "give the user a list of the links of news separately as well that you got from the response"
            f"\n{DISCLAIMER}"
        ]

        # Include stock-specific news if available
        if symbol and len(results) > 1:
            output.append(
                "Crawl the links in the data to understand Indian Stock News data:\n"
                f"{json.dumps(results[1], indent=2, ensure_ascii=False)}\n\n"
                "If not enough to understand try searching by yourself as well"
                "give the user a list of the links of news separately as well that you got from the response"
                f"\n{DISCLAIMER}"
            )

        return "\n\n".join(output)

    except requests.Timeout:
        return f"Error fetching news data: request timed out after 60 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error fetching news data: {exc}\n{TRY_LOGIN}"
