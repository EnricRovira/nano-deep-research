from pydantic import BaseModel, Field

from agents import Agent

PROMPT = (
    "You are a helpful research assistant."
    "Given a query, with a startup description, try to find information about this company."
    "Use the mission statement to help you find competitors."
    "\nMax 3 competitors to search for."
    "\nThe competitors should be from the same industry as the startup."
    "\nIf the region is global, search for competitors in english."
    "\nIf the region is not global, search for in the language of the region."
)


class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(
        description="A list of web searches to perform to best answer the query. 2-5 items are recommended."
    )

planner_agent = Agent(
    name="Planner Agent",
    instructions=PROMPT,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)