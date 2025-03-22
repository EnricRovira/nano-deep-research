# Agent used to synthesize a final report from the individual summaries.
from pydantic import BaseModel
from agents import Agent
from app.api.v1.responses.responses import CompetitorAnalysisResponse

PROMPT = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research "
    "assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
)

writer_agent = Agent(
    name="WriterAgent",
    instructions=PROMPT,
    model="o3-mini",
    output_type=CompetitorAnalysisResponse,
)