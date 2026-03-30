"""
Smart Exercise Runner
--------------------
Runs any exercise, automatically handling PYTHONPATH for project imports.
"""

import sys
import subprocess
import os
from pathlib import Path

EXERCISES = [
    "00a_basic_prompt.py",
    "00b_system_prompt.py",
    "00c_single_shot.py",
    "00d_few_shot.py",
    "01_llm_basics.py",
    "02_rag_intro.py",
    "03_agent_tools.py",
    "04_mcp_server.py",
]


def is_project_import_exercise(fname):
    # All exercises after 00d require project imports
    return fname >= "01_llm_basics.py"


def main():
    print("\nSmart Exercise Runner")
    for idx, fname in enumerate(EXERCISES, 1):
        print(f"{idx}. {fname}")
    choice = input("\nSelect an exercise to run: ").strip()
    try:
        idx = int(choice) - 1
        fname = EXERCISES[idx]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return
    script_path = Path(__file__).parent / fname
    if is_project_import_exercise(fname):
        # Use python -m exercises.filename (from project root)
        print(f"Running: python -m exercises.{fname[:-3]}")
        subprocess.run([sys.executable, "-m", f"exercises.{fname[:-3]}"])
    else:
        # Run directly
        print(f"Running: python {script_path}")
        subprocess.run([sys.executable, str(script_path)])

if __name__ == "__main__":
    main()
