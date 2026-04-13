"""
Exercise 03: Agent Tools
-----------------------
- Learn about agent tools and tool calling
- Try using the agent to answer a question that requires tool use

Instructions:
- Edit this file to try different agent queries and see tool reasoning steps.
"""



from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from dotenv import load_dotenv
import os
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain_core.tools import Tool
from core.llm_provider import LLMProvider
import requests
from langchain_community.tools.tavily_search import TavilySearchResults


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    # Directly create the tool and agent
    llm = LLMProvider().get_llm()
    wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

    def get_weather(city: str) -> str:
        """Get current weather for a city using OpenWeatherMap."""
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not api_key:
            return "Missing OPENWEATHERMAP_API_KEY in environment."

        # Normalize city input that may include extra quotes from the agent.
        city = city.strip().strip("\"'")

        try:
            weather_url = "https://api.openweathermap.org/data/2.5/weather"
            weather_params = {
                "q": city,
                "appid": api_key,
                "units": "metric",
            }
            weather_resp = requests.get(weather_url, params=weather_params, timeout=10)
            weather_resp.raise_for_status()
            weather_data = weather_resp.json()
            temp = weather_data.get("main", {}).get("temp")
            wind = weather_data.get("wind", {}).get("speed")
            condition = (weather_data.get("weather") or [{}])[0].get("description")
            return (
                f"Current temperature in {city}: {temp}°C, "
                f"wind speed: {wind} m/s, conditions: {condition}."
            )
        except Exception as e:
            return f"Weather lookup error for '{city}': {e}"

    weather_tool = Tool(
        name="get_weather",
        description="Get the current weather for a given city (e.g., 'San Francisco').",
        func=get_weather,
    )

    # Add Tavily web search tool with explicit usage guidance
    _tavily_search = TavilySearchResults()
    web_search_tool = Tool(
        name="web_search",
        description=(
            "Search the web for recent or time-sensitive facts like stock prices, "
            "news, or current events. Use for queries such as 'Oracle stock price yesterday'."
        ),
        func=_tavily_search.run,
    )

    tools = [wiki_tool, weather_tool, web_search_tool]
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        return_intermediate_steps=True,
        handle_parsing_errors=True,
    )

    # Try both Wikipedia and weather queries
    questions = [
        "What is the capital of France?",
        # "What is the weather in San Francisco?",
        # "What is the stock price of Oracle yesterday?"
    ]
    for question in questions:
        result = agent.invoke({"input": question})
        print("\nQuestion:", question)
        print("Answer:", result.get("output", ""))
        # print("Steps:")
        # for action, observation in result.get("intermediate_steps", []):
        #     print(f"- Tool: {action.tool}")
        #     print(f"  Input: {action.tool_input}")
        #     print(f"  Observation: {observation}")
