from typing import List, Optional

from crewai import Agent, Task, LLM
from pydantic import BaseModel, Field
from tavily import TavilyClient

basic_llm = LLM(model="gpt-4o", temperature=0)
search_client = TavilyClient(api_key="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")


class VideoOutLines(BaseModel):
    video_name: str
    previous_video_name: Optional[str] = Field(default=None, title="The name of the previous video")
    video_keywords: List[str]
    video_description: str


class CourseOutLines(BaseModel):
    videos: List[VideoOutLines] = Field(..., title="List of video metadata that the course contains")
    course_skills: List[str] = Field(..., title="List of skills that the course covers")
    course_objectives: List[str] = Field(..., title="List of objectives that the course covers")


generate_course_outlines = Agent(
    role="Generata Outline for Course and keywords for web search",
    goal="\n".join([
        "You will be provided with some information about a course, including the course name and the target audience and the level of the course.",
        "Your task is to generate a complete course outline that includes:",
        "- The previous video name, in case first video, it will be None'",
        "- Clear and relevant video titles,",
        "- A description for each video for that is this video should be discussed in the course.",
        "- Up to 2 keywords per video for use in web search.",
        "",
        "It is essential that the content, structure, and language of all videos are aligned with the target audience's background, experience level, and learning needs.",
        "Ensure that every video is appropriate for the audience and contributes to a clear and logical progression throughout the course.",
    ]),
    backstory="You are the first AI in the process of generating professional course in specific domain, the next AI will use your output to generate the course.",
    llm=basic_llm,
    verbose=True,
)

search_queries_recommendation_task = Task(
    description="\n".join([
        "Your task is to create a professional course outline for {course_name}.",
        "The course must be designed specifically for {target_audience}.",
        "The level of the course is {course_level}.",
        "{note}"
        "",
        "Every video in the course must be aligned with the knowledge level, interests, and learning goals of the target audience.",
        "Make sure the course structure, terminology, and tone are tailored to suit the target audience throughout.",
        "",
        "For each video, provide:",
        "- A clear and relevant title.",
        "- A short description that reflects the video’s purpose and fits the audience level.",
        "- Up to 2 keywords suitable for web search that match the video topic and audience understanding.",
        "- The previous video name, in case first video, it will be None.",
        "",
        "Ensure the videos follow a logical, progressive structure and cover the course topic clearly."
    ]),
    expected_output="A JSON object containing a list of course outlines.",
    output_pydantic=CourseOutLines,
    agent=generate_course_outlines
)
