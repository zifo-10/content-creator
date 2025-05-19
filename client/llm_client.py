import os
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from constant_manager import valid_content_prompt, format_video_content, user_format_video_content
from model.llm_response import VideoContentLLMResponseList


class OpenAITextProcessor:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini", max_workers: int = 5):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)


    def get_valid_content(self, raw_content: str,
                          video_name: str,
                          video_description: str) -> str:
        try:
            if not raw_content:
                return ""
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    ChatCompletionSystemMessageParam(
                        role="system",
                        content=valid_content_prompt.replace("{video_name}", video_name),
                    ),
                    ChatCompletionUserMessageParam(
                        role="user",
                        content=f"You are a professional in generating course outlines,"
                                f" your task is to generate a valid content for the video name {video_name} and description {video_description},\n"
                                f"the content is: {raw_content}."
                    )
                ],
                temperature=0
            )
            return response.choices[0].message.content
        except Exception as e:
            raise e

    def generate_video(self, course_name: str, video_name: str, course_level: str,
                       video_description: str, target_audience: str, raw_content: list[str],
                       previous_video_name: str = "None") -> list[str]:
        try:
            if not previous_video_name:
                previous_video_name = "None"
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    ChatCompletionSystemMessageParam(
                        role="system",
                        content=format_video_content.
                        replace("{course_name}", course_name).
                        replace("{target_audience}", target_audience)
                    ),
                    ChatCompletionUserMessageParam(
                        role="user",
                        content=user_format_video_content.
                        replace("{course_name}", course_name).
                        replace("{previous_video_name}", previous_video_name).
                        replace("{video_name}", video_name).
                        replace("{video_description}", video_description).
                        replace("{course_level}", course_level).
                        replace("{target_audience}", target_audience).
                        replace("{raw_content}", str(raw_content))
                    )
                ],
                response_format=VideoContentLLMResponseList,
                temperature=0
            )
            return response.choices[0].message.parsed.video_content
        except Exception as e:
            raise e
