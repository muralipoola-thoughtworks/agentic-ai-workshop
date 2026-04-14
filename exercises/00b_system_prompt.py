"""
Exercise 00b: System Prompt (Plain LangChain)
--------------------------------------------
- Demonstrate use of a system prompt (context) with Ollama.

Prompting Tip: The RRR Formula
-----------------------------
Use the RRR formula to structure your prompts for better LLM results:

R = Role: Set the assistant's role or persona (e.g., "You are a helpful assistant...")
R = Request: Clearly state what you want (e.g., "Explain what a large language model is.")
R = Restriction: Add any constraints or requirements (e.g., "Use simple language and keep the answer under 100 words.")

This helps contextualize the LLM's role and restricts output to get the required outcome.
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

if __name__ == "__main__":
    llm = ChatOllama(model="mistral")

    # RRR Formula Example
    # Role: You are a helpful assistant that explains AI concepts simply.
    # Request: Explain what a large language model is.
    # Restriction: Use simple language and keep the answer under 50 words.
    system_prompt = "You are a helpful assistant that explains AI concepts simply."
    user_prompt = "Explain what a large language model is. Use simple language and keep the answer under 50 words."

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ])
    messages = prompt.format_messages()
    print("System Prompt (Role):", system_prompt)
    print("User Prompt (Request + Restriction):", user_prompt)
    print("Response:", llm.invoke(messages))
