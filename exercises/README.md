# Workshop Exercises

This folder contains step-by-step exercises for the GenAI Workshop. Each exercise builds on the previous one and is numbered for easy reference.

## Included Exercises

0a. **00a_basic_prompt.py** — Basic user prompt
0b. **00b_system_prompt.py** — System prompt (context)
0c. **00c_single_shot.py** — Single-shot prompt
0d. **00d_few_shot.py** — Few-shot (multi-shot) prompt
1. **01_llm_basics.py** — LLM basics and prompt completion (with framework)
2. **02_rag_intro.py** — RAG pipeline introduction and querying
3. **03_agent_tools.py** — Agent tool usage and reasoning
4. **04_mcp_server.py** — MCP server and tool API usage

## How to Use

- Follow the order above for a smooth learning path.
- Each exercise file contains instructions and code to run or modify.
- Refer to the main project README for setup and server instructions.

## How to Run Exercises

- To run a single exercise:
  ```bash
  python exercises/00a_basic_prompt.py
  # Replace with any other exercise filename
  ```
- To launch a menu and run any or all exercises interactively:
  ```bash
  python exercises/run_all_exercises.py
  ```
- To run any exercise with automatic handling (recommended):
  ```bash
  python exercises/run.py
  ```

## Mapping to Workshop Topics

| Workshop Topic                | Exercise File         |
|-------------------------------|----------------------|
| LLM Prompting (Basic)         | 00a, 00b, 00c, 00d   |
| LLM Concepts & Prompting      | 01_llm_basics.py     |
| Retrieval Augmented Generation| 02_rag_intro.py      |
| Agentic AI & Tool Use         | 03_agent_tools.py    |
| MCP & Tool APIs               | 04_mcp_server.py     |

> **Important:**
> Use Python 3.11 for all exercises. Python 3.12 is not supported by LangChain and Pydantic v1.
> 
> To create a compatible environment:
> ```bash
> uv venv --python=python3.11
> source .venv/bin/activate
> uv pip install -r requirements.txt
> ```

> **Note:**
> - Exercises 00a–00d can be run directly with `python exercises/filename.py`.
> - Exercises 01 and above import from your project modules and should be run with:
>   ```bash
>   python -m exercises.filename  # e.g. python -m exercises.01_llm_basics
>   ```
>   or:
>   ```bash
>   PYTHONPATH=. python exercises/filename.py
>   ```

