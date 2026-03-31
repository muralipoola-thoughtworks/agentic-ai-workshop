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
        """Get current weather for a city using Open-Meteo and Nominatim."""
        try:
            # Step 1: Geocode city name to lat/lon
            geo_url = f"https://nominatim.openstreetmap.org/search"
            geo_params = {"q": city, "format": "json", "limit": 1}
            geo_resp = requests.get(geo_url, params=geo_params, headers={"User-Agent": "agentic-ai-demo"}, timeout=10)
            geo_resp.raise_for_status()
            geo_data = geo_resp.json()
            if not geo_data:
                return f"Could not find location for '{city}'."
            lat = geo_data[0]["lat"]
            lon = geo_data[0]["lon"]

            # Step 2: Query Open-Meteo for current weather
            weather_url = "https://api.open-meteo.com/v1/forecast"
            weather_params = {
                "latitude": lat,
                "longitude": lon,
                "current_weather": "true",
            }
            weather_resp = requests.get(weather_url, params=weather_params, timeout=10)
            weather_resp.raise_for_status()
            weather_data = weather_resp.json()
            current = weather_data.get("current_weather")
            if not current:
                return f"Weather data not available for '{city}'."
            temp = current.get("temperature")
            wind = current.get("windspeed")
            desc = f"Current temperature in {city}: {temp}°C, wind speed: {wind} km/h."
            return desc
        except Exception as e:
            return f"Weather lookup error for '{city}': {e}"

    weather_tool = Tool(
        name="get_weather",
        description="Get the current weather for a given city (e.g., 'San Francisco').",
        func=get_weather,
    )

    # Add Tavily web search tool to the agent's tools
    web_search_tool = TavilySearchResults()

    tools = [wiki_tool, weather_tool, web_search_tool]
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        return_intermediate_steps=True,
    )

    # Try both Wikipedia and weather queries
    questions = [
        "What is the capital of France?",
        "What is the weather in San Francisco?",
        "Whata is the stock price of oracle yesterday?"
    ]
    for question in questions:
        result = agent.invoke({"input": question})
        print("\nQuestion:", question)
        print("Answer:", result.get("output", ""))
        print("Steps:")
        for action, observation in result.get("intermediate_steps", []):
            print(f"- Tool: {action.tool}")
            print(f"  Input: {action.tool_input}")
            print(f"  Observation: {observation}")
