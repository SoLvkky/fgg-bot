from bot import logger, settings
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient

client = MongoClient(settings.MONGO_LINK)
db = client.get_database("fgg_db")
games = db.get_collection("games")
settings_table = db.get_collection("settings")

def insert_game(obj: dict):
    game = {
        "store": obj.get("store"),
        "title": obj.get("title"),
        "link": obj.get("link"),
        "desc": obj.get("desc"),
        "poster": obj.get("poster"),
        "rating": obj.get("rating"),
        "rating_count": obj.get("rating_count"),
        "price": obj.get("price"),
        "release": obj.get("release"),
        "genres": obj.get("genres"),
        "expiry": obj.get("expiry")
    }

    new_game = get_game(game["link"])

    if new_game:
        games.insert_one(game)
        logger.info(f"New game added to database! {obj["store"]} - {obj["title"]}")
        return True
    else:
        return False

def get_game(link) -> bool:
    now = datetime.now(timezone.utc)
    month_ago = now - timedelta(days=30)

    db_game = games.find_one({
        "link": link,
    })

    if db_game:
        now = datetime.now(timezone.utc)
        month_ago = now - timedelta(days=30)
        old_game = games.find_one({
            "link": link,
            "expiry": {"$lt": month_ago}
        })
        if old_game:
            return True
        else:
            return False
    else:
        return True            

def insert_settings(obj: dict) -> bool | False:
    guild_exist = settings_table.find_one({
        "guild_id": obj.get("guild_id")
    })

    if guild_exist:
        settings_table.update_one({
            "guild_id": obj.get("guild_id")
        }, 
        {"$set": 
            {
            "channel_id": obj.get("channel_id"),
            "role_id": obj.get("role_id")
            }
        })
    
    else:
        guild_settings = {
            "guild_id": obj.get("guild_id"),
            "channel_id": obj.get("channel_id"),
            "role_id": obj.get("role_id"),
        }
        settings_table.insert_one(guild_settings)
    
    logger.info(f"New notifications configuration for guild {obj.get("guild_id")}")
    return True
    
def get_settings(guild_id: int = None):
    if guild_id:
        guild = settings_table.find_one({"guild_id": guild_id})
        channel_id = guild.get("channel_id")
        role_id = guild.get("role_id")

        return {"channel_id": channel_id, "role_id": role_id}            

    guild_settings = settings_table.find()
    result = []

    for i in guild_settings:
        result.append({
            "guild_id": i["guild_id"],
            "channel_id": i["channel_id"],
            "role_id": i["role_id"]
        })

    return result

def remove_settings(guild_id):
    guild_settings = settings_table.find_one({
        "guild_id": guild_id
    })

    if guild_settings:
        settings_table.update_one({
            "guild_id": guild_id
        }, 
        {"$set": 
            {
            "channel_id": None,
            "role_id": None
            }
        })
        logger.info(f"Notifications removed for guild {guild_id}")
        return True
    else:
        return False

def get_actual_offers(time = datetime.now(timezone.utc).isoformat()):
    return list(games.find({"expiry": {"$gte": time}}))