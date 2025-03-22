from pydantic import BaseSettings


class Settings(BaseSettings):
    #Takes default values, and overrides them with environment variables if they are present
    db_type: str = "postgresql"
    db_username: str = "postgres"
    db_password: str
    db_hostname: str = "localhost"
    db_port: str = "5432"
    db_name: str = "fastapi"
    JWT_secret_key: str
    JWT_ALGORITHM: str = "HS256"
    JWT_TOKEN_EXPIRE_MINUTES: int = 60*24

    class Config:
        env_file = ".env"


settings = Settings()


