import asyncio
from typing import List

import openai
from fastapi import HTTPException

from config import OPEN_AI_API_KEY
from logger import logger


openai.api_key = OPEN_AI_API_KEY


class ChatGPTClient:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model

    async def review_code(self, files: List[dict], candidate_level: str) -> str:
        files_text = "".join(
            f"\nFile: {file['file_path']}\n{file['file_content']}\n" for file in files)
        prompt = self.create_prompt(candidate_level, files_text)
        logger.info(f"Generated prompt: \n {prompt}")

        # print("promptprompt: ", prompt)
        attempts = 3
        response = None

        for attempt in range(attempts):
            try:
                logger.info(f"Sending prompt")
                response = await self.send_request(prompt)
            except openai.error.RateLimitError as err:
                if attempt < attempts - 1:
                    logger.info(f"Received a RateLimitError, next attempt in 30 seconds")
                    await asyncio.sleep(30)
                    continue
                else:
                    raise HTTPException(status_code=429, detail=err.json_body)

        logger.info(f"ChatGPT response: \n {response['choices'][0]['message']['content']}")
        return response['choices'][0]['message']['content']
        # return response['choices'][0]['message']['content']
        # return prompt

    async def send_request(self, prompt):
        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert code reviewer."},
                {"role": "user", "content": prompt}
            ]
        )

    def create_prompt(self, candidate_level, files):
        return f"""
        You are a code reviewer for a {candidate_level} developer. 
        Here are the files from their project:
        
        {files}

        Analyze the quality of the code, identify potential issues, and suggest improvements. 
        Provide a general overview and recommendations.
        """
