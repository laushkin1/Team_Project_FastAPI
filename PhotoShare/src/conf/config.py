from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    postgres_user: str = os.getenv('POSTGRES_USER') #'postgres'
    password: str = os.getenv('PASSWORD')
    port: int = os.getenv('PORT')
    db_name: str = os.getenv('DB_NAME')
    sqlalchemy_database_url: str = os.getenv('SQLALCHEMY_DATABASE_URL')
    secret_key: str = os.getenv('SECRET_KEY')
    algorithm: str = os.getenv('ALGORITHM')
    mail_username: str = os.getenv('MAIL_USERNAME')
    mail_password: str = os.getenv('MAIL_PASSWORD')
    mail_from: str = os.getenv('MAIL_FROM')
    mail_port: int = os.getenv('MAIL_PORT')
    mail_server: str = os.getenv('MAIL_SERVER')
    # redis_host: str = os.getenv('REDIS_HOST')
    # redis_port: int = os.getenv('REDIS_PORT')
    cloudinary_name: str = os.getenv('CLOUDINARY_NAME')
    cloudinary_api_key: str = os.getenv('CLOUDINARY_API_KEY')
    cloudinary_api_secret: str = os.getenv('CLOUDINARY_API_SECRET')

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()