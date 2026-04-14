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
import json
import os
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from core.llm_provider import LLMProvider
import requests
from langchain_tavily import TavilySearch


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    # Directly create the tool and agent
    llm = LLMProvider().get_llm()
    wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

    def _coerce_city(value) -> str:
        if isinstance(value, dict):
            city = value.get("city")
            return str(city) if city is not None else str(value)

        if isinstance(value, str):
            stripped = value.strip().strip("\"'")
            if stripped.startswith("{"):
                try:
                    parsed = json.loads(stripped)
                except json.JSONDecodeError:
                    return stripped
                if isinstance(parsed, dict) and "city" in parsed:
                    return str(parsed["city"])
            return stripped

        return str(value)

    @tool
    def get_weather(city: str) -> str:
        """Get current weather for a city using OpenWeatherMap."""
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not api_key:
            return "Missing OPENWEATHERMAP_API_KEY in environment."

        city = _coerce_city(city)

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

    @tool
    def wikipedia_search(query: str) -> str:
        """Search Wikipedia for a query."""
        return wiki_tool.run(query)

    # Add Tavily web search tool with explicit usage guidance
    _tavily_search = TavilySearch()

    @tool
    def web_search(query: str) -> str:
        """Search the web for recent or time-sensitive facts like stock prices or news."""
        return _tavily_search.run(query)

    tools = [wikipedia_search, get_weather, web_search]
    agent = create_agent(
        llm,
        tools=tools,
        system_prompt="You are a helpful assistant that can use tools.",
        debug=False,
    )

    # Try both Wikipedia and weather queries
    questions = [
        "What is the capital of France?",
        # "What is the weather in San Francisco?",
        # "What is the stock price of Oracle yesterday?"
    ]
    for question in questions:
        print("\nQuestion:", question)
        # print("--- Tool Steps ---")
        # for event in agent.stream(
        #     {"messages": [HumanMessage(content=question)]},
        #     stream_mode="messages",
        # ):
        #     if isinstance(event, tuple) and len(event) == 2:
        #         _, payload = event
        #     else:
        #         payload = event

        #     messages = payload.get("messages", []) if isinstance(payload, dict) else []
        #     for message in messages:
        #         message_type = type(message).__name__
        #         content = getattr(message, "content", "")
        #         if message_type in {"ToolMessage", "AIMessage"}:
        #             print(f"{message_type}: {content}")

        result = agent.invoke({"messages": [HumanMessage(content=question)]})
        messages = result.get("messages", [])
        answer = messages[-1].content if messages else ""
        print("Answer:", answer)
       
