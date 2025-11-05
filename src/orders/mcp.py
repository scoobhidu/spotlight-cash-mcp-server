import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, TRY_LOGIN

orders_mcp = FastMCP(name="Orders MCP")


@orders_mcp.tool(
    name="place_order",
    description="Place an order in the system with all required order details.",
)
def place_order(
        ctx: Context,
        symbol: Annotated[str, Field(description="Symbol of the instrument (e.g., RELIANCE, TCS, INFY)")],
        exchange: Annotated[Literal["NSE", "BSE"], Field(
            description="Exchange (NSE = National Stock Exchange, BSE = Bombay Stock Exchange)")],
        segment: Annotated[
            Literal["E", "D"], Field(description="Segment (E = Equity, D = Derivatives [Futures/Options])")],
        txn_type: Annotated[Literal["B", "S"], Field(description="Transaction type (B = Buy, S = Sell)")],
        order_type: Annotated[Literal["MKT", "LMT", "SL"], Field(
            description="Order type (MKT = Market, LMT = Limit, SL = Stop-Loss)")],
        quantity: Annotated[int, Field(description="Quantity to trade (shares or contracts)")],
        price: Annotated[float, Field(description="Price (required for LMT orders)")] = 0,
        trigger_price: Annotated[float, Field(description="Trigger price (for SL orders)")] = 0,
        product: Annotated[Literal["C", "M", "I"], Field(
            description="Product type (C = Cash/Delivery, M = Margin, I = Intraday)")] = "C",
        validity: Annotated[Literal["DAY", "IOC", "GTD", "EOS"], Field(
            description="Order validity (DAY = End of day, IOC = Immediate or Cancel, GTD = Good Till Date, EOS = End of Session for BSE FnO)")] = "DAY",
        disc_quantity: Annotated[int, Field(description="Disclosed quantity (visible to market)")] = 0,
        off_mkt_flag: Annotated[int, Field(description="Off-market flag (0 = Normal, 1 = Off-market)")] = 0,
        remarks: Annotated[str, Field(description="Remarks or notes for the order")] = "",
        client_id: Annotated[str, Field(description="Client ID for the trading account")] = "AA0793",
) -> str:
    url = f"{API_HOST}/place_order"
    headers = _build_api_headers(ctx.session_id)
    order_data = {
        "client_id": client_id, "symbol": symbol, "exchange": exchange,
        "segment": segment, "txn_type": txn_type, "order_type": order_type,
        "quantity": quantity, "price": price, "trigger_price": trigger_price,
        "product": product, "validity": validity, "disc_quantity": disc_quantity,
        "off_mkt_flag": off_mkt_flag, "remarks": remarks, "source": "W"
    }
    try:
        resp = requests.post(url, headers=headers, json=order_data, timeout=30)
        resp.raise_for_status()
        return f"Order placed successfully:\n{json.dumps(resp.json(), indent=2, ensure_ascii=False)}"
    except requests.RequestException as exc:
        return f"Error placing order: {getattr(exc.response, 'text', str(exc))}\n{TRY_LOGIN}"


@orders_mcp.tool(
    name="modify_order",
    description="Modify an existing order by providing updated details.",
)
def modify_order(
    ctx: Context,
    order_no: Annotated[str, Field(description="Order number to modify")],
    order_type: Annotated[Literal["MKT", "LMT", "SL"], Field(description="New order type (MKT, LMT, SL)")],
    quantity: Annotated[int, Field(description="New quantity for the order")],
    price: Annotated[float, Field(description="New price (for LMT orders)")]=0,
    trigger_price: Annotated[float, Field(description="New trigger price (for SL orders)")]=0,
    validity: Annotated[Literal["DAY", "IOC", "GTD", "EOS"], Field(description="New validity (DAY, IOC, GTD, EOS)")]="DAY",
    disc_quantity: Annotated[int, Field(description="New disclosed quantity")]=0,
    off_mkt_flag: Annotated[int, Field(description="Off-market flag (0 = Normal, 1 = Off-market)")]=0,
    remarks: Annotated[str, Field(description="Remarks for modification")] = "",
    client_id: Annotated[str, Field(description="Client ID for trading account")] = "AA0793",

) -> str:
    url = f"{API_HOST}/modify_order"
    headers = _build_api_headers(ctx.session_id)
    modify_data = {
        "client_id": client_id, "order_no": order_no, "order_type": order_type,
        "quantity": quantity, "price": price, "trigger_price": trigger_price,
        "validity": validity, "disc_quantity": disc_quantity,
        "off_mkt_flag": off_mkt_flag, "remarks": remarks, "source": "W"
    }
    try:
        resp = requests.post(url, headers=headers, json=modify_data, timeout=30)
        resp.raise_for_status()
        return f"Order modified successfully:\n{json.dumps(resp.json(), indent=2, ensure_ascii=False)}"
    except requests.RequestException as exc:
        return f"Error modifying order: {getattr(exc.response, 'text', str(exc))}\n{TRY_LOGIN}"


@orders_mcp.tool(
    name="cancel_order",
    description="Cancel an existing order using its order number.",
)
def cancel_order(
    ctx: Context,
    order_no: Annotated[str, Field(description="Order number to cancel")],
    client_id: Annotated[str, Field(description="Client ID for trading account")] = "",
) -> str:
    url = f"{API_HOST}/cancel_order"
    headers = _build_api_headers(ctx.session_id)
    cancel_data = {
        "client_id": client_id,
        "order_no": order_no,
        "source": "W"
    }
    try:
        resp = requests.post(url, headers=headers, json=cancel_data, timeout=30)
        resp.raise_for_status()
        return f"Order cancelled successfully:\n{json.dumps(resp.json(), indent=2, ensure_ascii=False)}"
    except requests.RequestException as exc:
        return f"Error cancelling order: {getattr(exc.response, 'text', str(exc))}\n{TRY_LOGIN}"
