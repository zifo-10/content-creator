import os
from typing import Any

from dotenv import load_dotenv
from tavily import TavilyClient

from client.llm_client import OpenAITextProcessor

load_dotenv()

search_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_web(keywords: list[str], video_name: str, video_description: str) -> list[Any] | None:
    try:
        raw_content_list = []
        llm_client = OpenAITextProcessor()
        for keyword in keywords:
            web_search = search_client.search(
                query=keyword,
                max_results=1,
                include_raw_content=True
            )
            for result in web_search["results"]:
                valid_content = llm_client.get_valid_content(
                    raw_content=result["raw_content"] if result["raw_content"] else "",
                    video_name=video_name,
                    video_description=video_description)
                print("valid_content********", valid_content)
                raw_content_list.append(valid_content)
        return raw_content_list
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
