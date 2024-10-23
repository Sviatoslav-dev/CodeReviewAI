from fastapi import FastAPI

from chatgpt_client import ChatGPTClient
from github_client import GithubRepo
from pydantic_models import ReviewResponse, ReviewRequest
from repositories_cache import RepositoriesCache

app = FastAPI()


@app.post("/review", response_model=ReviewResponse)
async def review_assignment(review_request: ReviewRequest):
    github_client = GithubRepo(review_request.github_repo_url)
    chat_gpt_client = ChatGPTClient()

    repo_cache = RepositoriesCache()
    cached_review = await repo_cache.check_repo(
        github_client, review_request.github_repo_url, review_request.candidate_level)

    if cached_review:
        return ReviewResponse(**cached_review)

    files = await github_client.get_files()

    review_result = await chat_gpt_client.review_code(files, review_request.candidate_level)

    review_response = ReviewResponse(found_files=str([file["file_path"] for file in files]),
                                     review_result=str(review_result))

    await repo_cache.add_data(time=86400, data=review_response)

    return review_response
