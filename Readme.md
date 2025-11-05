# Spotlight Cash MCP server
This repository contains an implementation of an MCP (Model Context Protocol) Server, which allows seamless integration between external systems and AI assistants that support MCP.

# Overview
This repository contains a suite of data services that work together to:
- Handle authenticated “session” creation and message flow (backed by an AWS SQS).
- Uses Ventura Securities' and Nifty Trader's data APIs for getting the financial data of a financial instrument.
- Provide an MCP-oriented financial instrument valuation service with login and notification listening.

It’s designed to be simple to run locally while remaining cloud-ready.

## Capabilities
You can explore as much as you want with this MCP server.
- Forecast a stock's price based on GARP or DCF model evaluations
- Create hedge strategies that are delta neutral and more inclined towards your preference be it stock-based or index-based. If you are looking for covered calls or synthetic collar based strategies.
- Understand technicals, fundamentals, valuations and then trade scrips smartly.
- Identify chart patterns of 1Day, 1Week, 1Month, 1Year etc. for finding good technical setups.
- Analyse your trading patterns using your trade reports or understand charges in your ledger summary.
- Start and end your day by asking the market cues to stay updated around the financial markets of the world. 
- You can ask opinions on your custom strategies and if they have a high probability of profit.
- Ask which stocks are approaching an indicator like golden cross or death cross
- See if any stocks from your portfolio require rotation based on some kind of indicator that you follow
- Ask suggestions on which IPOs to apply for? takes considerations from GMP present on chittorgarh.in
- Fetch volume boomers to gain an edge on trading NSE stocks that have unusually high volume. 
and many more

## Features
- Session service with queue integration (e.g., AWS SQS).
- Data service for financial data feeding to LLMs
- MCP service with SSO authentication and long-running notification listening.
- Clean separation of concerns so each service can be scaled independently.

## Requirements
- Python 3.11.9
- virtualenv (for an isolated environment)
- OS: macOS, Linux, or Windows
- Possibly a CRON service to download the master files(bhavcopy) daily from your broker or a vendor to remain updated if any stock's name or nse, nfo or bse token has been changed

## Quick start
1) Create and activate a virtual environment
2) Sync the packages from requirements.txt
3) You can either run the project using Docker Compose or
you can run the server_data.py and server_mcp.py file on different ports