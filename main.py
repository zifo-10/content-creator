from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional

from fastapi.middleware.cors import CORSMiddleware

from controller import generate_course_content
from model.content_dto import VideoOutLinesWithContent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CourseRequest(BaseModel):
    course_name: str
    target_audience: str
    course_level: str
    notes: Optional[str] = Field(default=None, title="Additional notes for the course generation")

@app.post("/generate-course", response_model=List[VideoOutLinesWithContent])
def generate_course(request: CourseRequest):
    return generate_course_content(
        course_name=request.course_name,
        target_audience=request.target_audience,
        course_level=request.course_level,
        notes=request.notes
    )
