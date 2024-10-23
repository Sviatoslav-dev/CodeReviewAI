import hashlib
import json

import redis.asyncio as redis
from config import REDIS_URL
from logger import logger


class RepositoriesCache:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        self.cache_key = None

    async def check_repo(self, github_client, repo_url, candidate_level):
        latest_commit_sha = await github_client.get_latest_commit_sha()

        self.cache_key = hashlib.sha256(
            f"{repo_url}:{latest_commit_sha}:{candidate_level}".encode()).hexdigest()

        cached_review = await self.redis_client.get(self.cache_key)
        if cached_review:
            logger.info(f"Found cached review for {repo_url}")
            cached_review_data = json.loads(cached_review)
            return cached_review_data

    async def add_data(self, time, data):
        await self.redis_client.setex(
            self.cache_key, time=time, value=json.dumps(data.dict()))
