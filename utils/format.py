import asyncio
from services import get_deals, get_game_via_steam, get_steam_details, get_token, get_data
from database import get_game, insert_game
from aiohttp import ClientSession

async def format_deals(session: ClientSession):
    deals = []

    token_task = get_token(session)
    epic_task = get_deals(session, "epic")
    steam_task = get_deals(session, "steam")

    token, epic_deals, steam_deals = await asyncio.gather(
        token_task, epic_task, steam_task
    )
    
    if epic_deals:
        for deal in epic_deals:
            deal["platform"] = "Epic Games Store"
            deals.append(deal)
    if steam_deals:
        for deal in steam_deals:
            deal["platform"] = "Steam"
            deals.append(deal)
    
    tasks = [process_deal(session, token, deal) for deal in deals]
    results = await asyncio.gather(*tasks)

    result = [r for r in results if r is not None]
    
    return result

async def process_deal(session: ClientSession, token: str, deal: dict):
    
    new_game = get_game(deal.get("link"))
    if not new_game:
        return None
    
    content = {
        "store": deal.get("platform"),
        "price": deal.get("price"),
        "link": deal.get("link"),
        "desc": deal.get("desc"),
        "expiry": deal.get("expiry")
    }

    igdb_answer = await get_data(session, token, link=deal.get("link"))
    
    if igdb_answer["success"]:
        data = igdb_answer.get("data")
        data.update(content)
        return data
    
    steam_game = await get_game_via_steam(session, deal.get("title"))
    if not steam_game:
        return deal
    
    igdb_new_answer = await get_data(session, token, link=steam_game.get("link"))
    
    if igdb_new_answer["success"]:
        data = igdb_new_answer.get("data")
        data.update(content)
        return data
    
    steam_details = await get_steam_details(session, [steam_game.get("id")])
    steam_details.update(content)
    return steam_details

async def check_games():
    async with ClientSession() as session:
        res = await format_deals(session)
        result = []

        for i in res:
            new = insert_game(i)
            if new:
                result.append(i)

        return result