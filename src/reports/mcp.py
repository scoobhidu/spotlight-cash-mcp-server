import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, TRY_LOGIN

reports_mcp = FastMCP(name="Reports Service")



@reports_mcp.tool(
    name="get_user_ledger_reports",
    description="A summary of all your transactions including the buy/sell orders, pay-ins and withdrawals, by default keep current indian financial year start and end date",
)
def get_user_ledger_reports(
    ctx: Context,
    from_date: Annotated[str, Field(description="Start date to fetch the report data, keep in format 19-Aug-25")],
    end_date: Annotated[str, Field(description="End date to fetch the report data, keep in format 19-Aug-25")],
) -> str:
    url = f"{API_HOST}/ledger_reports"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, json={
            "from_date": from_date, "to_date": end_date
        }, timeout=180)
        response.raise_for_status()

        return (
            f"{response.json()}"
            f"{DISCLAIMER}"
        )

    except requests.Timeout:
        return f"Error fetching ledger reports\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error fetching ledger reports: {getattr(exc.response, 'text', str(exc))}\n{TRY_LOGIN}"


@reports_mcp.tool(
    name="email_user_ledger_reports",
    description="Email the user a summary of all your transactions including the buy/sell orders, pay-ins and withdrawals, by default keep current indian financial year start and end date",
)
def email_user_ledger_reports(
    ctx: Context,
    from_date: Annotated[str, Field(description="Start date to fetch the report data, keep in format 19-Aug-25")],
    end_date: Annotated[str, Field(description="End date to fetch the report data, keep in format 19-Aug-25")],
) -> str:
    url = f"{API_HOST}/email_ledger_reports"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, json={
            "from_date": from_date, "to_date": end_date}, timeout=180)
        response.raise_for_status()

        return (
            f"{response.json()}"
            f"{DISCLAIMER}"
        )

    except requests.Timeout:
        return f"Error emailing ledger reports\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error emailing ledger reports: {getattr(exc.response, 'text', str(exc))}\n{TRY_LOGIN}"


@reports_mcp.tool(
    name="get_ledger_bill_details",
    description="A details of all your transactions for the buy/sell bill notes",
)
def get_user_ledger_details(
    ctx: Context,
    bill_no: Annotated[str, Field(description="Bill number to fetch details for a ledger entry")],
) -> str:
    url = f"{API_HOST}/ledger_bill_details"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, json={
            "sbillno": bill_no,
        }, timeout=180)
        response.raise_for_status()

        return (
            f"{response.json()}"
            f"{DISCLAIMER}"
        )

    except requests.Timeout:
        return f"Error fetching ledger reports\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error fetching ledger reports: {getattr(exc.response, 'text', str(exc))}\n{TRY_LOGIN}"


@reports_mcp.tool(
    name="download_user_holding_reports",
    description="A details of all the user's holdings for the last trading day",
)
def download_user_holding_reports(
    ctx: Context,
) -> str:
    url = f"{API_HOST}/download_holding_reports"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, json={}, timeout=180)
        response.raise_for_status()

        return f"show the url generated in this response: {response.json()}, ask the user to click on this link and upload the file for holding reports analysis"

    except requests.Timeout:
        return f"Error downloading holding reports\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error downloading holding reports: {getattr(exc.response, 'text', str(exc))}\n{TRY_LOGIN}"


@reports_mcp.tool(
    name="trade_reports_summary",
    description="A record of all the trades made on the user's account including buy/sell price and quantities, by default keep current indian financial year start and end date",
)
def trade_reports_summary(
    ctx: Context,
    from_date: Annotated[str, Field(description="Start date to fetch the report data, keep in format 19-Aug-25")],
    end_date: Annotated[str, Field(description="End date to fetch the report data, keep in format 19-Aug-25")],
) -> str:
    url = f"{API_HOST}/trade_reports_summary"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, json={
            "from_date": from_date, "to_date": end_date}, timeout=180)
        response.raise_for_status()

        return (
            f"{response.json()}"
            f"{DISCLAIMER}"
        )

    except requests.Timeout:
        return f"Error downloading trade reports\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error downloading trade reports: {getattr(exc.response, 'text', str(exc))}\n{TRY_LOGIN}"


@reports_mcp.tool(
    name="trade_details_report",
    description="A record of all the trades made on the user's account including buy/sell price and quantities for a particular trade id, by default keep current indian financial year start and end date",
)
def trade_details_report(
    ctx: Context,
    from_date: Annotated[str, Field(description="Start date to fetch the report data, keep in format 19-Aug-25")],
    end_date: Annotated[str, Field(description="End date to fetch the report data, keep in format 19-Aug-25")],
    scrip_code: Annotated[str, Field(description="Scrip Code of the trade report to look into")],
) -> str:
    url = f"{API_HOST}/trade_details_report"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, json={
            "scrip_code": scrip_code,
            "from_date": from_date, "to_date": end_date}, timeout=180)
        response.raise_for_status()

        return (
            f"{response.json()}"
            f"{DISCLAIMER}"
        )

    except requests.Timeout:
        return f"Error downloading trade details reports\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error downloading trade details reports: {getattr(exc.response, 'text', str(exc))}\n{TRY_LOGIN}"


@reports_mcp.tool(
    name="email_trade_reports",
    description="Email a record of all the trades made on the user's account including buy/sell price and quantities from a particular date to an end date, by default keep current indian financial year start and end date",
)
def email_trade_reports(
    ctx: Context,
    from_date: Annotated[str, Field(description="Start date to fetch the report data, keep in format 19-Aug-25")],
    end_date: Annotated[str, Field(description="End date to fetch the report data, keep in format 19-Aug-25")],
) -> str:
    url = f"{API_HOST}/email_trade_reports"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, json={
            "from_date": from_date, "to_date": end_date}, timeout=180)
        response.raise_for_status()

        return response.json()

    except requests.Timeout:
        return f"Error emailing trade reports\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error emailing trade reports: {getattr(exc.response, 'text', str(exc))}\n{TRY_LOGIN}"


@reports_mcp.tool(
    name="get_tax_reports",
    description="Get a record of the tax report indicating realised profit/loss over short term/long term from a particular date to an end date, by default keep current indian financial year start and end date",
)
def get_tax_reports(
    ctx: Context,
    from_date: Annotated[str, Field(description="Start date to fetch the report data, keep in format 19-Aug-25")],
    end_date: Annotated[str, Field(description="End date to fetch the report data, keep in format 19-Aug-25")],
) -> str:
    url = f"{API_HOST}/get_tax_reports"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, json={
            "from_date": from_date, "to_date": end_date}, timeout=180)
        response.raise_for_status()

        return (
            f"{response.json()}"
            f"{DISCLAIMER}"
        )

    except requests.Timeout:
        return f"Error getting tax reports\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error getting tax reports: {getattr(exc.response, 'text', str(exc))}\n{TRY_LOGIN}"


@reports_mcp.tool(
    name="email_tax_reports",
    description="Email a record of the tax report indicating realised profit/loss over short term/long term from a particular date to an end date, by default keep current indian financial year start and end date",
)
def email_tax_reports(
    ctx: Context,
    from_date: Annotated[str, Field(description="Start date to fetch the report data, keep in format 19-Aug-25")],
    end_date: Annotated[str, Field(description="End date to fetch the report data, keep in format 19-Aug-25")],
) -> str:
    url = f"{API_HOST}/email_tax_reports"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, json={
            "from_date": from_date, "to_date": end_date}, timeout=180)
        response.raise_for_status()

        return response.json()

    except requests.Timeout:
        return f"Error emailing tax reports\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error emailing tax reports: {getattr(exc.response, 'text', str(exc))}\n{TRY_LOGIN}"


@reports_mcp.tool(
    name="get_dividend_report",
    description="Get a record of the dividend report received by the user for the stocks held in their Ventura demat account from a particular date to an end date, by default keep current indian financial year",
)
def get_dividend_report(
    ctx: Context,
    financial_year: Annotated[str, Field(description="Financial year to fetch the report data, keep in format 2025-2026")],
) -> str:
    url = f"{API_HOST}/get_dividend_report"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, json={"from_year": financial_year}, timeout=180)
        response.raise_for_status()

        return (
            f"{response.json()}"
            f"{DISCLAIMER}"
        )

    except requests.Timeout:
        return f"Error getting dividend reports\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error getting dividend reports: {getattr(exc.response, 'text', str(exc))}\n{TRY_LOGIN}"


@reports_mcp.tool(
    name="email_daily_activity_statement",
    description="Email a record of the daily activity report received by the user for the fund transfers and collateral pledged from a particular date to an end date, by default keep indian last working date",
)
def email_daily_activity_statement(
    ctx: Context,
    date: Annotated[str, Field(description="Date to fetch the report data, keep in format 19-Aug-25")],
) -> str:
    url = f"{API_HOST}/email_daily_activity_statement"
    headers = _build_api_headers(ctx.session_id)

    try:
        response = requests.post(url, headers=headers, json={
            "from_date": date,}, timeout=180)
        response.raise_for_status()

        return response.json()

    except requests.Timeout:
        return f"Error emailing daily activity reports\n{TRY_LOGIN}"
    except requests.RequestException as exc:
        return f"Error emailing daily activity reports: {getattr(exc.response, 'text', str(exc))}\n{TRY_LOGIN}"

