from agents import Agent, WebSearchTool, FunctionTool
from agents.model_settings import ModelSettings
from agents.run_context import RunContextWrapper
from tavily import AsyncTavilyClient
import os
from pydantic import BaseModel, Field
import logging
from dotenv import load_dotenv, find_dotenv
from app.utils.logger import setup_logging
from app.schemas.competitor import CompetitorAnalysisResponse
setup_logging(
    None,
    level=logging.INFO
)

load_dotenv(find_dotenv('.env'))

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you must:"
    "\nUse the search_tavily tool to search the web for the term"
    "\n1. IMMEDIATELY after receiving search results, fill the info in the output data model"
    "\n2. Return ONLY the output data model as your final response without ANY additional commentary"
    "\n3.Focus on how to fill the output model data based on the search results following these guidelines:"
    "\For the pricing plan if the competitor its an ecommerce use the one-time-purchase"
)

# Initialize Tavily client outside the function to reuse it
tavily_api_key = os.getenv("KEY_TAVILY")
print(f"Tavily API key: {tavily_api_key}")
if not tavily_api_key:
    logging.warning("No Tavily API key found. The search tool will not work without an API key.")

tavily_client = AsyncTavilyClient(api_key=tavily_api_key)

async def search_tavily(
    query: str,
    self_domain_url: str
) -> str:
    """Search the web using Tavily's API and return relevant results.
    
    Args:
        query: The search query to use for retrieving information from the web.
    """
    if not tavily_api_key:
        return "Error: Tavily API key is not configured. Please set the TAVILY_API_KEY environment variable."
    
    if not query:
        return "Error: No search query provided."
    
    try:
        response = await tavily_client.search(
            query=query,
            search_depth="basic",
            max_results=5,
            include_answer=True,
            include_domains=self_domain_url
        )
        
        if not response.get("results"):
            return "No results found for your query."
        else:
            logging.info(f"Search completed for query: {response.get('query')} in {response.get('response_time')} seconds")
        
        # Format the results
        formatted_results = []
        
        # Include Tavily's generated answer at the top if available
        if response.get("answer"):
            formatted_results.append(f"Tavily Summary: {response.get('answer')}\n")
            
        # Include individual results
        for i, result in enumerate(response.get("results", [])):
            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")
            formatted_results.append(f"Source {i+1}: Url:{url}\nTitle: {title}\nContent: {content}\n")
        
        return "\n".join(formatted_results)
    
    except Exception as e:
        logging.error(f"Error searching Tavily: {str(e)}")
        raise Exception(f"Error searching Tavily: {str(e)}")

# Define the function arguments
class FunctionArgs(BaseModel):
    query: str = Field(..., description="The search query to use for retrieving information from the web.")
    
    class Config:
        extra = "forbid"  # This will make additionalProperties=false in the JSON schema


async def run_function(ctx: RunContextWrapper, args: str) -> str:
    try:
        parsed = FunctionArgs.model_validate_json(args)
        include_domains = []
        if ctx.context and "self_domain_url" in ctx.context:
            domain = ctx.context.get("self_domain_url")
            if domain:
                include_domains = [domain]
                logging.info(f"Using domain filter from context: {domain}")
        print(f"Query: {parsed.query}")
        print(f"Include domains: {include_domains}")
        result = await search_tavily(
            query=parsed.query,
            self_domain_url=include_domains,
        )
        logging.info(f"Search completed for query: {parsed.query}")
        return result
    except Exception as e:
        import sys
        sys.exit(1)
        logging.error(f"Error in run_function: {str(e)}")
        return f"Error performing search: {str(e)}"


tool = FunctionTool(
    name="search_tavily",
    description="Search the web using Tavily's API and return relevant results.",
    params_json_schema={
        **FunctionArgs.model_json_schema(),
        "additionalProperties": False
    },
    on_invoke_tool=run_function,
)

# Create the search agent with Tavily search tool
search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[tool],
    model_settings=ModelSettings(
        temperature=0.3,
        tool_choice="auto",
    ),
    model="gpt-4o-mini",
    output_type=CompetitorAnalysisResponse,
)