from aiohttp import ClientSession
from time import perf_counter

async def ping():
    async with ClientSession() as session:
        steam_status, steam_time = await response(session, "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2?appid=10&count=1")
        epic_status, epic_time = await response(session, "https://store-content.ak.epicgames.com/api/en-us/content/products/fortnite")
        igdb_status, igdb_time = await response(session, "https://api.igdb.com/v4/game")

        return {
            "steam": {
                "status": True if steam_status == 200 else False,
                "ping": steam_time
            },
            "epic": {
                "status": True if epic_status == 200 else False,
                "ping": epic_time
            },
            "igdb": {
                "status": True if igdb_status == 401 else False,
                "ping": igdb_time
            },
        }
    
async def response(session: ClientSession, url: str):
    time_start = perf_counter()
    async with session.get(url=url) as resp:
        await resp.read()
        time_end = perf_counter()
        time = round((time_end - time_start) * 1000, 2)
        status = resp.status

    return status, time