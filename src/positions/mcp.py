import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, DISCLAIMER, TRY_LOGIN

positions_mcp = FastMCP(name="Positions MCP")

@positions_mcp.tool(
    name="get_user_positions_summary",
    description="Fetch and return the current user's positions summary with P&L details and open positions.",
)
def get_user_positions_summary(
    ctx: Context,
) -> str:
    url = f"{API_HOST}/get_user_positions_summary"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, json={}, timeout=30)
        response.raise_for_status()
        positions_data = response.json()

        summary = {
            "profit_loss_summary": {
                "total_profit_or_loss": positions_data.get("total_profit_or_loss"),
                "realised_profit_or_loss": positions_data.get("realised_profit_or_loss"),
                "unrealised_profit_or_loss": positions_data.get("unrealised_profit_or_loss"),
            },
            "open_positions_count": len(positions_data.get("open_positions", [])),
            "open_positions": positions_data.get("open_positions", []),
        }

        return (
            "Current positions summary:\n\n"
            f"📊 **Profit/Loss Summary:**\n"
            f"• Total P&L: ₹{summary['profit_loss_summary']['total_profit_or_loss']}\n"
            f"• Realised P&L: ₹{summary['profit_loss_summary']['realised_profit_or_loss']}\n"
            f"• Unrealised P&L: ₹{summary['profit_loss_summary']['unrealised_profit_or_loss']}\n\n"
            f"📈 **Open Positions:** {summary['open_positions_count']} position(s)\n\n"
            f"{json.dumps(summary, indent=2, ensure_ascii=False)}"
            f"{DISCLAIMER}"
        )

    except requests.Timeout:
        return f"Error fetching positions summary: request timed out after 30 seconds\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error fetching positions summary: {getattr(exc.response, 'text', str(exc))}\n{TRY_LOGIN}"