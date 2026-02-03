from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str
    TEST_GUILD_ID: int
    GUILD_LOGS: int
    TV_ID: str
    TV_SECRET: str
    MONGO_LINK: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()