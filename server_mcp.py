import asyncio

from fastapi import HTTPException
from fastmcp import FastMCP, Context
from pydantic import ConfigDict, BaseModel, Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.chart_router.mcp import charts_mcp
from config import connection_headers, SSO_LOGIN_URL
from src.global_indices.mcp import global_indices_mcp
from src.holdings.mcp import holdings_mcp
from src.indian_news.mcp import news_mcp
from src.ipo.mcp import ipo_mcp
from src.options.mcp import options_mcp
from src.orders.mcp import orders_mcp
from src.positions.mcp import positions_mcp
from src.reports.mcp import reports_mcp
from src.research.mcp import research_mcp
from src.sectoral_indices.mcp import indian_sector_mcp
from src.stock_corporate_actions.mcp import corporate_actions_mcp
from src.stock_financials.mcp import financial_mcp
from src.stock_fundamentals.mcp import fundamental_mcp
from src.stock_marketwatch.mcp import equity_mktwatch_mcp
from src.fno_marketwatch.mcp import fno_mktwatch_mcp
from src.stock_overview.mcp import overview_mcp
from src.stock_technicals.mcp import technical_mcp
from src.valuation.miscellaneous_tools import miscellaneous_mcp
from src.volume_boomers.mcp import volume_boomers_mcp


# Represents payload data for creating an MCP session.
#
# This class is designed to encapsulate and validate the required data for
# the validation of incoming session tokens post login to invest.venturasecurities.com dashboard.
# These tokens are then parsed and massaged to this Payload Class
class CreateMCPSessionPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    connection_id: str
    authorization: str = Field(alias="Authorization")
    session_id: str
    client_id: str


mcp = FastMCP(name="Spotlight")

@mcp.custom_route("/create_mcp_session", methods=["POST"])
async def create_mcp_session(request: Request):
    payload = await request.json()
    try:
        connection_headers[payload['connection_id']] = {
            "Authorization": payload['Authorization'],
            "session_id": payload['session_id'],
            "client_id": payload['client_id'],
        }

        return JSONResponse({"message": "Session created", "connection_id": payload['connection_id']})

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create session")


# Login to Ventura's Spotlight for trading information and order placement. This function is
# a tool-calling function essential for initiating and interacting with Ventura's account through AI.
#
# The login process includes showing a warning message about the use of AI systems and providing the
# user with a login link. The user is expected to follow the link in their browser to complete the
# authentication process.
#
# Without the login tool called and successfully completed, the spotlight tools will not work for any MCP client.
@mcp.tool(
    name="login",
    description="Login to Ventura's Spotlight for trading info and order placement, essential for tool calling",
)
def login(ctx: Context) -> str:
    return f'''
IMPORTANT: Please display this warning to the user before proceeding:
⚠️ **WARNING: AI systems are unpredictable and non-deterministic. By continuing, you agree to interact with your Ventura account via AI at your own risk.**
After showing the warning above, provide the user with this login link: [Login to Spotlight]({SSO_LOGIN_URL}?mcp_connection_id={ctx.session_id})
If your client supports clickable links, you can render and present it and ask them to click the link above. Otherwise, display the URL and ask them to copy and paste it into their browser: {SSO_LOGIN_URL}?mcp_connection_id={ctx.session_id}
After completing the login in your browser, let me know and I'll continue with your request.
                    '''


# Runs the MCP server by importing multiple server modules and starting the HTTP server
# with specified configurations.
#
# This asynchronous function initializes various MCP server modules sequentially and
# then starts the main HTTP server on the specified host and port. Each server module
# corresponds to a distinct component, feature, or data service within the MCP framework.
async def run_mcp_server():
    await mcp.import_server(equity_mktwatch_mcp)
    await mcp.import_server(fno_mktwatch_mcp)
    await mcp.import_server(research_mcp)
    await mcp.import_server(ipo_mcp)
    await mcp.import_server(volume_boomers_mcp)
    await mcp.import_server(reports_mcp)
    await mcp.import_server(technical_mcp)
    await mcp.import_server(overview_mcp)
    await mcp.import_server(orders_mcp)
    await mcp.import_server(charts_mcp)
    await mcp.import_server(options_mcp)
    await mcp.import_server(news_mcp)
    await mcp.import_server(positions_mcp)
    await mcp.import_server(fundamental_mcp)
    await mcp.import_server(financial_mcp)
    await mcp.import_server(corporate_actions_mcp)
    await mcp.import_server(global_indices_mcp)
    await mcp.import_server(holdings_mcp)
    await mcp.import_server(indian_sector_mcp)
    await mcp.import_server(miscellaneous_mcp)

    await mcp.run_http_async(host="0.0.0.0", port=10001, log_level="DEBUG")


if __name__ == "__main__":
    try:
        asyncio.run(run_mcp_server())
    except KeyboardInterrupt:
        pass