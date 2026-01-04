import logging

from pydantic_settings import BaseSettings, SettingsConfigDict
import httpx
from mcp.server.fastmcp import FastMCP


class Config(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env")

    URL: str
    X_BOT_SECRET: str


config = Config()

HEADERS = {"x-bot-secret": config.X_BOT_SECRET}

mcp = FastMCP("transactions")


@mcp.tool()
async def get_transactions() -> str:
    """Get cash transactions of the user."""

    async with httpx.AsyncClient(headers=HEADERS) as client:
        response = await client.get(config.URL)
        return response.text


def main():

    logging.basicConfig(
        filename="transactions_server.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    logging.info("Starting Transactions MCP Server")

    mcp.run(transport="stdio")

    logging.info("Transactions MCP Server stopped")


if __name__ == "__main__":
    main()
