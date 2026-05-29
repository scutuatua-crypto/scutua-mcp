@app.tool()
async def get_smart_money_flows() -> dict:
    """Get smart money wallet flows from Dune Analytics"""
    cache_key = "dune:smart_money_flows"
    cached = get_cached(cache_key)
    if cached:
        return cached
    if not DUNE_API_KEY:
        return {"error": "DUNE_API_KEY not configured"}
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://api.dune.com/api/v1/query/7607813/results",
                headers={"x-dune-api-key": DUNE_API_KEY},
                timeout=15
            )
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=300)
            return data
    except Exception as e:
        logger.error(f"Smart money flows error: {e}")
        return {"error": str(e)}
