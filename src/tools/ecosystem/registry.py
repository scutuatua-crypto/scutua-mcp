from .heartbeat import ecosystem_heartbeat
from .biometrics import project_biometrics
from .intelligence import ecosystem_intelligence, what_should_i_build
from .narrative import ecosystem_narrative

def register_ecosystem_tools(app):
    
    @app.tool()
    async def ecosystem_heartbeat_tool() -> str:
        """🫀 Scutua Nervous System pulse — ecosystem alive status + stats"""
        result = await ecosystem_heartbeat()
        return str(result)

    @app.tool()
    async def project_biometrics_tool(project_id: str = "") -> str:
        """🧬 Health check for all projects or specific project by ID"""
        result = await project_biometrics(project_id if project_id else None)
        return str(result)

    @app.tool()
    async def ecosystem_intelligence_tool() -> str:
        """🧠 Cross-project analysis and insights"""
        result = await ecosystem_intelligence()
        return str(result)

    @app.tool()
    async def what_should_i_build_tool() -> str:
        """🚀 AI-powered next move advisor for the ecosystem"""
        result = await what_should_i_build()
        return str(result)

    @app.tool()
    async def ecosystem_narrative_tool() -> str:
        """📖 Auto-generate today's Scutua ecosystem story"""
        result = await ecosystem_narrative()
        return str(result)
