import re

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

EPIC_API_URL = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US"
EPIC_BASE_URL = "https://store.epicgames.com/p/"
STEAM_FREE_URL = "https://store.steampowered.com/search/?maxprice=free&category1=998&specials=1&ndl=1"
STEAM_SEARCH_URL = "https://store.steampowered.com/search/"
STEAM_API_URL = "https://store.steampowered.com/api/appdetails"
STEAM_BASE_URL = "https://store.steampowered.com/app/"

default_headers = {
    'Accept-Language': 'en-US',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'
}

async def get_deals(session: ClientSession, platform):
    match platform:
        case "steam":
            ids = await get_steam_deals(session)
            if ids:
                return await get_steam_details(session, ids)
        case "epic":
            return await get_epic_deals(session)   

async def get_expiry(session: ClientSession, id: int):
    async with session.get(url=f"{STEAM_BASE_URL}{id}", headers=default_headers) as response:
        data = BeautifulSoup(await response.text(), "html.parser")

        expiry = data.select_one("p.game_purchase_discount_quantity").text.strip()
        
        if expiry:
            match = re.search(r'before (\w{3} \d{1,2}) @ (\d{1,2}:\d{2})(am|pm)', expiry)

            if match:
                date_part = match.group(1)
                time_part = match.group(2)
                ampm = match.group(3)
                year = datetime.now().year
                
                date_str = f"{date_part} {year} {time_part} {ampm}"

                dt = datetime.strptime(date_str, '%b %d %Y %I:%M %p')
                dt = dt + timedelta(hours=8)
                
                utc_iso = dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
                return utc_iso
                    
        else:
            return

async def get_steam_deals(session: ClientSession):
    async with session.get(url=STEAM_FREE_URL, headers=default_headers) as response:
        data = BeautifulSoup(await response.text(), "html.parser")
        ids = []

        try:
            search_result = data.select_one("div#search_resultsRows").select("a")

            if search_result:
                for i in search_result:
                    steam_id = i.get("data-ds-appid")
                    ids.append(steam_id)
            
            return ids

        except Exception:
            return []
            
async def get_game_via_steam(session: ClientSession, game: str):
    params = {
        "term": game,
        "supportedlang": "english"
    }

    async with session.get(url=STEAM_SEARCH_URL, params=params, headers=default_headers) as response:
        data = BeautifulSoup(await response.text(), "html.parser")

        try:
            search_result = data.select_one("div#search_resultsRows").select_one("a")

            if search_result:
                title = search_result.select_one("div.search_name.ellipsis").text.strip()
                steam_id = search_result.get("data-ds-appid")
                href = '/'.join(search_result.get("href").split('/')[:-2])
                return {"id": steam_id, "title": title, "link": href}
            
        except Exception:
            return None

async def get_steam_details(session: ClientSession, ids: list):

    url = STEAM_API_URL
    res = []

    for id in ids:
        params = {
                "appids": id,
                "cc": "us"
        }

        async with session.get(url=url, params=params, headers=default_headers) as response:
            data = await response.json()
            status = data[str(id)]["success"]
            if status:
                result = data[str(id)]["data"]
                title = result.get("name")
                poster = result.get("header_image")
                price = float(result.get("price_overview").get("initial"))/100
                desc = result.get("short_description").strip()
                expiry = await get_expiry(session, id) or None

                genres_list = result.get("genres")
                genres = []
                for i in genres_list:
                    genres.append(i.get("description"))

                res.append({
                    "title": title,
                    "desc": desc,
                    "poster": poster,
                    "price": price,
                    "link": f"{STEAM_BASE_URL}{id}",
                    "expiry": expiry
                })
            else:
                continue

    return res

async def get_epic_deals(session: ClientSession):
    async with session.get(url=EPIC_API_URL, headers=default_headers) as response:
        data = await response.json()
        result = data["data"]["Catalog"]["searchStore"]["elements"]

        games = []

        for i in result:
            if (i.get("status") == "ACTIVE" and i.get("price").get("totalPrice").get("discountPrice") == 0):
                title = i.get("title")
                poster = i.get("keyImages")[0].get("url")
                desc = i.get("description").strip()
                price = float(i.get("price").get("totalPrice").get("fmtPrice").get("originalPrice").replace("$", "")) or 0.00
                url = i.get("offerMappings")[0].get("pageSlug")
                expiry = i.get("promotions").get("promotionalOffers")[0].get("promotionalOffers")[0].get("endDate")

                games.append({
                    "title": title,
                    "desc": desc,
                    "poster": poster,
                    "price": price,
                    "link": f"{EPIC_BASE_URL}{url}",
                    "expiry": expiry
                })

        return games