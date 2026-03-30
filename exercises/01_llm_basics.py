"""
Exercise 01: LLM Basics
----------------------
- Learn what an LLM is
- Run a simple prompt through the configured LLM

Instructions:
- Edit this file to experiment with LLM prompts and outputs.
"""

from core.llm_provider import LLMProvider

if __name__ == "__main__":
    llm = LLMProvider().get_llm()
    prompt = "What is a large language model? Explain in simple terms."
    print("Prompt:", prompt)
    print("Response:", llm.invoke(prompt))
