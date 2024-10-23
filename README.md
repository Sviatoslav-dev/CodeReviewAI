# Part 1

## How to run locally

First, you need to clone the repository, create a virtual environment, and navigate to the project directory.

Then install the dependencies by
```
pip install dist/codereviewai-0.1.0-py3-none-any.whl
```

Fill in the config file OPEN_AI_API_KEY and GITHUB_TOKEN in comfig.py.

Start the Redis container by
```
docker-compose up --build
```

Run the application:
```
uvicorn main:app --reload
```

Then, send a POST request to url http://127.0.0.1:8000/review with body wich has assignment_description, github_repo_url and candidate_level, 
for example
```
{
    "assignment_description": "This is echo server with asyncio",
    "github_repo_url": "https://github.com/Sviatoslav-dev/asyncio_echo_server",
    "candidate_level": "junior"
}
```


Caching works as follows: it checks whether a request has already been made with the same repository, the latest commit (no updates in the repository), and the developer's level. If such a request was made before, the previously saved review is returned.

For GPT API requests, a retry with a 30-second delay is set to handle minute-based rate limits.

For unit tests, I mocked the Redis client.

# Part 2
To resolve the issue with rate limits on the GitHub API or OpenAI GPT API, you can take the following approach. First, set your own rate limit. If the number of requests approaches the rate limit constraints of the GitHub API or OpenAI GPT API, you can increase the waiting time for users.

With large repositories, you can proceed as follows. First, analyze the overall structure of the repository, such as file structure, class diagrams, and similar. Then, break the repository into parts and make separate requests to GPT, providing information about the overall structure as well as the specific part.

Users will likely use this service continuously while working on their project. Therefore, it's worth adding user authentication, allowing them to use their GitHub token. Additionally, store information about the user’s repositories and enable reviewing individual commits or pull requests.
