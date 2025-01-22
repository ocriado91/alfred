"""Alfred - A personalized AI Agent."""

from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from dotenv import load_dotenv
from langchain_groq import ChatGroq

import argparse

# Load environment variables from .env file
load_dotenv()

wip_calendar = [
    """2025/01/25 Rock Concert.""",
    """2025/01/22 19:00 Avengers Meeting""",
    """2025/01/25 10:30 Run.""",
    """2025/06/08 10:30 Vintage Run Race.""",
]


class GoogleCalendarTool(BaseTool):
    """CrewAI Custom Tool to handle Google Calendar."""

    name: str = "Retrieve Google Calendar events."
    description: str = (
        "Handle Google calendar events to retrieve incoming events."
    )

    def _run(self) -> str:
        dates = []
        for line in wip_calendar:
            dates.append(line.split(" - ")[0])
        return ",".join(dates)


def argument_parser() -> argparse.ArgumentParser:
    """Parser incoming arguments."""
    args = argparse.ArgumentParser()
    args.add_argument("--request", required=True, help="User request")
    args.add_argument(
        "--model", default="groq/llama3-70b-8192", help="LLM Model to use."
    )
    args.add_argument(
        "--verbose",
        default=False,
        type=bool,
        help="Flag to enable verbose mode.",
    )
    return args.parse_args()


if __name__ == "__main__":
    try:
        # Parse arguments
        args = argument_parser()

        # Define LLM
        llm = ChatGroq(
            temperature=0.2,
            model_name=args.model,
        )

        # Define Agent
        google_calendar_reader = Agent(
            llm=llm,
            role="Professional extractor dates from Google Calendar according \
                to user request: {request}.",
            goal="Extract the events from a given tool to you.",
            backstory="You are an expert in retrieving Google Calendar dates.",
            verbose=args.verbose,
            tools=[GoogleCalendarTool()],
        )

        # Define Tasks
        event_task = Task(
            description="Retrieve events from calendar.",
            expected_output=(
                "In this task you should extract all relevant dates for a \
                    given request of the user."
                "Use tools available to you to accomplish this task."
                "The task output must be a string."
            ),
            agent=google_calendar_reader,
        )

        # Assemble Crew
        crew = Crew(
            agents=[google_calendar_reader],
            tasks=[event_task],
            verbose=args.verbose,
            process=Process.sequential,
        )

        # Execute crew
        crew_output = crew.kickoff(inputs={"request": args.request})

        # Accessing the crew output
        print(f"Raw Output: {crew_output.raw}")
        print(f"Tasks Output: {crew_output.tasks_output}")
        print(f"Token Usage: {crew_output.token_usage}")
        print(f"Metrics: {crew.usage_metrics}")
    except KeyboardInterrupt:
        pass
