# Agent used to synthesize a final report from the individual summaries.
from pydantic import BaseModel
from agents import Agent
from agents.model_settings import ModelSettings
from app.schemas.competitor import CompetitorAnalysisResponse

PROMPT = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research "
    "assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "Try to deduplicate data, dont hallucinate if you dont have the data.\n"
    "The data to put in the self_analysis field is the same as the Original query website.\n"
)

writer_agent = Agent(
    name="WriterAgent",
    instructions=PROMPT,
    model="gpt-4o-mini",
    output_type=CompetitorAnalysisResponse,
    model_settings=ModelSettings(
        temperature=0.25,
        max_tokens=6_000,
    ),
)