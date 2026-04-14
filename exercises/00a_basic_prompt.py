"""
Exercise 00a: Basic Prompt (Plain LangChain)
-------------------------------------------
- Run a simple user prompt using LangChain and Ollama.
"""

from langchain_ollama import OllamaLLM

if __name__ == "__main__":
    llm = OllamaLLM(model="mistral")
    prompt = "What is a large language model?"
    print("Prompt:", prompt)
    print("Response:", llm.invoke(prompt))
