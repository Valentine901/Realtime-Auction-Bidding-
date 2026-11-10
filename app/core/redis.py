import redis.asyncio as redis 
from app.core.config import setting

def create_redis() -> redis.Redis:
    # decode_responses=True gives back normal text instead of bytes like b"hello
    return redis.from_url(setting.REDIS_URL, decode_responses=True)