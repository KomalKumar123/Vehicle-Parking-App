import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Config:
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a-default-fallback-secret-key')
    
    
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'a-very-secure-jwt-secret-key')
    
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///../instance/parking.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  

    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # Cache configuration
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'SimpleCache') # Use 'RedisCache' for production
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL', 'redis://localhost:6379/1')
    CACHE_DEFAULT_TIMEOUT = 300 # Default cache expiry in seconds (5 minutes)
