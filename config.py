from pydantic_settings  import BaseSettings
import os

class Settings(BaseSettings):
    POSTGRES_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str
    SQLALCHEMY_DATABASE_URI: str
    ENCRYPTION_KEY: str
    ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SENDGRID_API_KEY: str
    SENDGRID_ADMIN_MAIL: str
    OPENAI_API_KEY: str
    MILVUS_PORT: int
    MILVUS_HOST: str
    

    class Config:
        # mode = os.getenv("MODE")
        # print(">>>>", mode)
        # if mode == "development" :
        #     env_file = "./.env.development"
        # else:
              env_file = "./.env.local"

env_variables = Settings()


