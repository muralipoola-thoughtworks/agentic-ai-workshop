"""
Exercise Launcher: Run All Exercises
-----------------------------------
This script lets you run any or all workshop exercises from a menu.
"""

import subprocess
import sys
import os

EXERCISES = [
    ("00a_basic_prompt.py", "Basic user prompt"),
    ("00b_system_prompt.py", "System prompt (context)"),
    ("00c_single_shot.py", "Single-shot prompt"),
    ("00d_few_shot.py", "Few-shot (multi-shot) prompt"),
    ("01_llm_basics.py", "LLM basics and prompt completion (with framework)"),
    ("02_rag_intro.py", "RAG pipeline introduction and querying"),
    ("03_agent_tools.py", "Agent tool usage and reasoning"),
    ("04_mcp_server.py", "MCP server and tool API usage"),
]


def print_menu():
    print("\nWorkshop Exercise Launcher")
    for idx, (fname, desc) in enumerate(EXERCISES, 1):
        print(f"{idx}. {fname} — {desc}")
    print(f"{len(EXERCISES)+1}. Run ALL exercises (except MCP server)")
    print(f"{len(EXERCISES)+2}. Exit")


def run_exercise(idx):
    fname, desc = EXERCISES[idx]
    print(f"\n--- Running: {fname} ---")
    subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), fname)])


def main():
    while True:
        print_menu()
        choice = input("\nSelect an exercise to run: ").strip()
        try:
            num = int(choice)
        except ValueError:
            print("Invalid input. Enter a number.")
            continue
        if 1 <= num <= len(EXERCISES):
            run_exercise(num-1)
        elif num == len(EXERCISES)+1:
            # Run all except MCP server (last one)
            for idx in range(len(EXERCISES)-1):
                run_exercise(idx)
        elif num == len(EXERCISES)+2:
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
