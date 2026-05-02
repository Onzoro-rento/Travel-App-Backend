from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    SQL_ECHO: bool = False
    SUPABASE_JWT_SECRET: str
    SUPABASE_URL: str = "https://your-project-ref.supabase.co"
    GOOGLE_PLACES_API_KEY: str = ""


settings = Settings()  # type: ignore[call-arg]
