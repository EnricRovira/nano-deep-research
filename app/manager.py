from __future__ import annotations

import asyncio
import time
import logging

from rich.console import Console

from agents import Runner, custom_span, gen_trace_id, trace, RunConfig

from app.agents.planner_agent import WebSearchItem, WebSearchPlan, planner_agent
from app.agents.search_agent import search_agent
from app.schemas.competitor import CompetitorAnalysisResponse
from app.schemas.competitor import Competitor
from app.schemas.request import CompetitorAnalysisRequest
from app.agents.writer_agent import writer_agent
from app.utils.printer import Printer


class ResearchManager:
    def __init__(self):
        self.console = Console()
        self.printer = Printer(self.console)

    async def run(self, request: CompetitorAnalysisRequest) -> None:
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            self.printer.update_item(
                "trace_id",
                f"View trace: https://platform.openai.com/traces/{trace_id}",
                is_done=True,
                hide_checkmark=True,
            )

            self.printer.update_item(
                "starting",
                "Starting research...",
                is_done=True,
                hide_checkmark=True,
            )
            search_plan = await self._plan_searches(request)
            search_results = await self._perform_searches(search_plan, self_url=request.website)
            report = await self._write_report(request, search_results)

            return report

    async def _plan_searches(self, query: str) -> WebSearchPlan:
        self.printer.update_item("planning", "Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
            max_turns=2
        )
        self.printer.update_item(
            "planning",
            f"Will perform {len(result.final_output.searches)} searches",
            is_done=True,
        )
        return result.final_output_as(WebSearchPlan)


    async def _perform_searches(self, search_plan: WebSearchPlan, self_url: str) -> list[str]:
        with custom_span("Search the web"):
            self.printer.update_item("searching", "Searching...")
            num_completed = 0
            tasks = [
                asyncio.create_task(self._search(item, self_url)) for item in search_plan.searches
            ]
            results = []
            for task in asyncio.as_completed(tasks):
                result = await task
                if result is not None:
                    results.append(result)
                num_completed += 1
                self.printer.update_item(
                    "searching", f"Searching... {num_completed}/{len(tasks)} completed"
                )
            self.printer.mark_item_done("searching")
            return results

    async def _search(self, item: WebSearchItem, self_url: str) -> str | None:
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input,
                max_turns=2, #IMPORTANT: This is to avoid calling the search tool more than once
                context={
                    "self_domain_url": self_url
                }
            )
            return str(result.final_output)
        except Exception as e:
            logging.error(f"Error during search: {str(e)}")
            return None
        

    async def _write_report(self, query: str, search_results: list[str]) -> CompetitorAnalysisResponse:
        self.printer.update_item("writing", "Thinking about report...")
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = Runner.run_streamed(
            writer_agent,
            input,
        )
        update_messages = [
            "Thinking about report...",
            "Planning report structure...",
            "Writing outline...",
            "Creating sections...",
            "Cleaning up formatting...",
            "Finalizing report...",
            "Finishing report...",
        ]

        last_update = time.time()
        next_message = 0
        async for _ in result.stream_events():
            if time.time() - last_update > 5 and next_message < len(update_messages):
                self.printer.update_item("writing", update_messages[next_message])
                next_message += 1
                last_update = time.time()

        self.printer.mark_item_done("writing")
        return result.final_output_as(CompetitorAnalysisResponse)