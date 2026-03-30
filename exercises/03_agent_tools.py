"""
Exercise 03: Agent Tools
-----------------------
- Learn about agent tools and tool calling
- Try using the agent to answer a question that requires tool use

Instructions:
- Edit this file to try different agent queries and see tool reasoning steps.
"""

from modules.agents.agent import RetailAgent

if __name__ == "__main__":
    agent = RetailAgent()
    question = "Where is my order ORD-1002 and should I escalate?"
    result = agent.run(question)
    print("Question:", question)
    print("Answer:", result.get("answer", ""))
    print("Steps:")
    for step in result.get("steps", []):
        print(f"- Tool: {step.get('tool')}")
        print(f"  Input: {step.get('input')}")
        print(f"  Observation: {step.get('observation')}")
