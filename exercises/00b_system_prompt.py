"""
Exercise 00b: System Prompt (Plain LangChain)
--------------------------------------------
- Demonstrate use of a system prompt (context) with Ollama.
"""

from langchain_community.llms import Ollama
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

if __name__ == "__main__":
    llm = Ollama(model="mistral")
    system_prompt = "You are a helpful assistant that explains AI concepts simply."
    user_prompt = "What is a large language model?"
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ])
    messages = prompt.format_messages()
    print("System Prompt:", system_prompt)
    print("User Prompt:", user_prompt)
    print("Response:", llm.invoke(messages))
