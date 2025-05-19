from crewai import Crew, Process
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

from client.llm_client import OpenAITextProcessor
from model.content_dto import VideoOutLinesWithContent, VideoOutLinesDTO
from outlines import generate_course_outlines, search_queries_recommendation_task
from web_search import search_web


def generate_course_content(
        course_name: str,
        target_audience: str,
        course_level: str,
        notes: str = "",
        about_company: str = "You are professional in generating course outlines."
) -> list[VideoOutLinesWithContent]:
    try:
        llm_client = OpenAITextProcessor()

        company_context = StringKnowledgeSource(content=about_company)

        course_crew = Crew(
            agents=[generate_course_outlines],
            tasks=[search_queries_recommendation_task],
            process=Process.sequential,
            knowledge_sources=[company_context]
        )

        crew_results = course_crew.kickoff(
            inputs={
                "course_name": course_name,
                "target_audience": target_audience,
                "course_level": course_level,
                "note": notes
            }
        )

        videos_outline_list = [
            VideoOutLinesDTO(
                video_name=video.video_name,
                previous_video_name=video.previous_video_name,
                video_keywords=video.video_keywords,
                video_description=video.video_description,
                course_skills=crew_results.pydantic.course_skills,
                course_objectives=crew_results.pydantic.course_objectives
            )
            for video in crew_results.pydantic.videos
        ]

        video_with_raw_content = []
        for video in videos_outline_list:
            video_content = search_web(
                keywords=video.video_keywords,
                video_name=video.video_name,
                video_description=video.video_description
            )
            video_with_raw_content.append(
                VideoOutLinesWithContent(
                    video_name=video.video_name,
                    previous_video_name=video.previous_video_name,
                    video_keywords=video.video_keywords,
                    video_description=video.video_description,
                    course_skills=video.course_skills,
                    course_objectives=video.course_objectives,
                    raw_content=video_content
                )
            )

        video_with_valid_content = []
        for video in video_with_raw_content:
            video_content = llm_client.generate_video(
                course_name=course_name,
                video_name=video.video_name,
                video_description=video.video_description,
                target_audience=target_audience,
                raw_content=video.raw_content,
                course_level=course_level,
                previous_video_name=video.previous_video_name
            )
            video_with_valid_content.append(
                VideoOutLinesWithContent(
                    video_name=video.video_name,
                    previous_video_name=video.previous_video_name,
                    video_keywords=video.video_keywords,
                    video_description=video.video_description,
                    course_skills=video.course_skills,
                    course_objectives=video.course_objectives,
                    raw_content=video_content
                )
            )

        return video_with_valid_content
    except Exception as error:
        print(f"An error occurred: {error}")
        raise error