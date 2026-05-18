"""🐙 GitHub Tool — Repo Operations"""

import os
from github import Github
from mcp.server.fastmcp import FastMCP
from src.utils.logger import get_logger
from src.utils.security import mask_secret

logger = get_logger(__name__)

def register_github_tools(app: FastMCP):
    g = Github(os.getenv("GH_TOKEN"))

    @app.tool()
    async def list_repos() -> list:
        """List all repos in WhaleTrucker ecosystem"""
        try:
            user = g.get_user()
            repos = [r.name for r in user.get_repos()]
            logger.info(f"📦 Found {len(repos)} repos")
            return repos
        except Exception as e:
            logger.error(f"GitHub error: {mask_secret(str(e))}")
            return []

    @app.tool()
    async def get_repo_status(repo_name: str) -> dict:
        """Get repo status, branches, and last commit"""
        try:
            user = g.get_user()
            repo = user.get_repo(repo_name)
            return {
                "name": repo.name,
                "private": repo.private,
                "default_branch": repo.default_branch,
                "last_commit": repo.get_commits()[0].sha[:7],
                "stars": repo.stargazers_count,
            }
        except Exception as e:
            logger.error(f"Repo error: {mask_secret(str(e))}")
            return {}
