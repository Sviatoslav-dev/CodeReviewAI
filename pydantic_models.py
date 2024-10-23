from pydantic import BaseModel, HttpUrl, Field


class ReviewRequest(BaseModel):
    assignment_description: str = Field(..., min_length=10, max_length=1000)
    github_repo_url: HttpUrl
    candidate_level: str = Field(..., pattern="^(junior|middle|senior)$")


class ReviewResponse(BaseModel):
    found_files: str
    review_result: str
