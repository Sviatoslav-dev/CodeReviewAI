from typing import List

import aiohttp
from fastapi import HTTPException

from config import GITHUB_TOKEN
from logger import logger


class GithubRepo:
    def __init__(self, github_repo_url):
        repo_info = str(github_repo_url).rstrip("/").split("/")[-2:]
        self.owner, self.repo = repo_info[0], repo_info[1]

        self.commits_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/commits"
        self.contents_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/"

    async def get_latest_commit_sha(self) -> str:
        async with aiohttp.ClientSession(
                headers={"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else None,
        ) as session:
            logger.info(f"Sending request {self.commits_url} to fetch commits")
            async with session.get(self.commits_url) as response:
                logger.info(f"{response.status} {await response.text()}")
                if response.status != 200:
                    raise HTTPException(status_code=response.status,
                                        detail=f"Failed to fetch commits from {self.commits_url}")
                commits = await response.json()
                return commits[0]["sha"]

    async def fetch_files_from_path(self, session, path=""):
        full_url = self.contents_url + path
        contents = await self.get_content(session, full_url)
        files = []
        for item in contents:
            if item["type"] == "file":
                file_path = path + item["name"]
                file_url = item["download_url"]

                file_content = await self.get_content(session, file_url)

                files.append({
                    "file_path": file_path,
                    "file_content": file_content
                })

            elif item["type"] == "dir":
                sub_path = path + item["name"] + "/"
                sub_files = await self.fetch_files_from_path(session, sub_path)
                files.extend(sub_files)

        return files

    async def get_content(self, session, url):
        async with session.get(url) as response:
            logger.info(f"Sending request {url}")
            logger.info(f"Received {response.status} { await response.text()}")
            if response.status != 200:
                raise HTTPException(status_code=response.status,
                                    detail=f"Failed to fetch contents from {url}")

            response = await response.json() \
                if response.content_type == 'application/json' else await response.text()
        return response

    async def get_files(self) -> List[dict]:
        async with aiohttp.ClientSession(
                headers={"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else None
        ) as session:
            files = await self.fetch_files_from_path(session)

        return files
