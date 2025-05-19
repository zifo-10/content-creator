from typing import Optional, List

from pydantic import BaseModel, Field


class VideoOutLinesDTO(BaseModel):
    video_name: str
    previous_video_name: Optional[str] = Field(default=None, title="The name of the previous video")
    video_keywords: List[str]
    video_description: str
    course_skills: List[str] = Field(..., title="List of skills that the course covers")
    course_objectives: List[str] = Field(..., title="List of objectives that the course covers")


class VideoOutLinesWithContent(VideoOutLinesDTO):
    raw_content: Optional[List[str]] = Field(None, description="The raw content retrieved from the web search")
