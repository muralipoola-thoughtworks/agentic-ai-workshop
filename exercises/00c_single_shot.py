"""
Exercise 00c: Single-shot Prompt (Plain LangChain)
-------------------------------------------------
- Show a single user question with a system prompt.
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

if __name__ == "__main__":
    llm = ChatOllama(model="mistral")
    system_prompt = "You are a helpful assistant that explains AI concepts simply."
    user_prompt = "Explain neural networks in simple terms."
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ])
    messages = prompt.format_messages()
    print("System Prompt:", system_prompt)
    print("User Prompt:", user_prompt)
    print("Response:", llm.invoke(messages))
