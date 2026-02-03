from aiohttp import ClientSession
from bot import settings

twitch_auth = "https://id.twitch.tv/oauth2/token"
game_data_url = "https://api.igdb.com/v4/games"

async def get_token(session: ClientSession):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "client_id": settings.TV_ID,
        "client_secret": settings.TV_SECRET,
        "grant_type": "client_credentials"
    }

    res = await session.post(twitch_auth, headers=headers, data=data)
    
    if res.status == 200:
        result = await res.json()
        token = result.get("access_token")

    else:
        return "Error in Twitch Authentication"

    return token

async def get_data(session: ClientSession, token: str, name: str = None, link: str = None):
    headers = {
        "Client-ID": settings.TV_ID,
        "Authorization": f"Bearer {token}"
    }

    if name:
        search = f'name = "{name}"'

    if link:
        search = f'external_games.url = "{link}"'
        
    if name and link:
        return {
            "success": False,
            "status": "Too many positional arguments"
        }
    
    data = f'''fields name, cover.*, genres.*, release_dates.*, external_games.*, total_rating, total_rating_count; 
    where {search} & game_type = 0;
    limit 1;'''
    
    res = await session.post(game_data_url, headers=headers, data=data)

    if res.status == 200:
        result_json = await res.json()
        result = result_json[0] if len(result_json) > 0 else None

        if isinstance(result, dict):
            cover = result.get("cover")
            genres_list = result.get("genres") or []
            release = result.get("release_dates")
            rating = result.get("total_rating")
            genres = []
            if genres_list:
                for i in genres_list:
                    genres.append(i.get("name"))

            return {
                "success": True,
                "data": {
                    "title": result.get("name"),
                    "poster": f"https:{cover.get("url").replace("thumb", "cover_big").replace("jpg", "webp")}" if cover else None,
                    "genres": genres,
                    "release": release[0].get("human") if release else "Unknown",
                    "rating": round(rating, 2) if rating else "Not rated",
                    "rating_count": result.get("total_rating_count") or 0
                    }
                }
        else:
            return {
                "success": False,
                "status": f"API OK, Game *{name or ''}* not found"
            }

    else:
        return {
            "success": False,
            "status": f"API ERROR: {res.status}"
        }