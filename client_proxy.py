import asyncio

from fastmcp import Client, FastMCP


async def run():
    async with Client("http://localhost:10001/mcp") as connected_client:
        proxy = FastMCP.as_proxy(connected_client)
        await proxy.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(run())