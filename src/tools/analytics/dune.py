"""
🧠 Dune Analytics Tools — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx
import os

DUNE_API_KEY = os.getenv("DUNE_API_KEY", "")

def register_dune_tools(app: FastMCP):

    @app.tool()
    async def execute_dune_query(query_id: int) -> dict:
        """Execute a Dune Analytics query and return results"""
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"https://api.dune.com/api/v1/query/{query_id}/execute",
                headers={"x-dune-api-key": DUNE_API_KEY}
            )
        execution_id = r.json().get("execution_id")
        return {"execution_id": execution_id, "query_id": query_id}

    @app.tool()
    async def get_dune_results(execution_id: str) -> dict:
        """Get results from a Dune Analytics execution"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://api.dune.com/api/v1/execution/{execution_id}/results",
                headers={"x-dune-api-key": DUNE_API_KEY}
            )
        return r.json()

    @app.tool()
    async def get_dune_latest_results(query_id: int) -> dict:
        """Get latest cached results from a Dune query"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://api.dune.com/api/v1/query/{query_id}/results",
                headers={"x-dune-api-key": DUNE_API_KEY}
            )
        return r.json()

