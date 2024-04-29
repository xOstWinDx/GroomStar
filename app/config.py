from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class AuthJWT(BaseModel):
    private_key_path: Path = Path("private.pem")
    public_key_path: Path = Path("public.pem")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    auth_jwt: AuthJWT = AuthJWT()

    SECRET_KEY: str
    ALGORITHM: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
