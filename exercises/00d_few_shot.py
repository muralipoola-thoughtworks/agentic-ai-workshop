"""
Exercise 00d: Few-shot Prompt (Reverse) - Customer Satisfaction Classification
-----------------------------------------------------------------------------
- Demonstrate few-shot prompting for classification tasks.
- Given an incoming customer email, classify the customer's satisfaction/tone (e.g., happy, sad, angry, excited, apologetic, neutral).

Instructions:
- Run this file and observe how the LLM classifies the tone/satisfaction of incoming emails.
- Try changing the examples or adding new tones to see how the model adapts.
"""

from langchain_community.llms import Ollama
from langchain_core.messages import SystemMessage, HumanMessage

if __name__ == "__main__":
    llm = Ollama(model="mistral")
    system_prompt = "You are a customer support assistant. Given an email from a customer, classify their satisfaction/tone as one of: happy, sad, angry, excited, apologetic, neutral. Reply with only the tone."
    # Few-shot examples: incoming emails and their classified tone
    examples = [
        ("Subject: Thank you!\n\nHi team, I just received my order and I'm thrilled with the service. Everything was perfect!", "happy"),
        ("Subject: Disappointed\n\nMy order arrived late and the product was damaged. I'm really upset about this experience.", "angry"),
        ("Subject: Order Delay\n\nHello, I noticed my order is delayed. Can you please update me on the status?", "neutral"),
        ("Subject: Amazing support\n\nThank you so much for your quick response and help with my issue!", "excited"),
        ("Subject: Sorry for the confusion\n\nI realized I made a mistake in my previous message. Sorry for any trouble caused.", "apologetic"),
        ("Subject: Not what I expected\n\nI'm a bit sad that the product didn't meet my expectations.", "sad")
    ]
    user_email = "Subject: Frustrated with my order\n\nI've been waiting for weeks and still haven't received my package. This is unacceptable."
    messages = [SystemMessage(content=system_prompt)]
    for email, tone in examples:
        messages.append(HumanMessage(content=email))
        messages.append(HumanMessage(content=tone))  # Simulate assistant reply for few-shot
    messages.append(HumanMessage(content=user_email))
    print("System Prompt:", system_prompt)
    print("Examples (email → tone):")
    for email, tone in examples:
        print(f"Email:\n{email}\nTone: {tone}\n")
    print("User Email:\n", user_email)
    print("Predicted Tone:", llm.invoke(messages))

    print("\nTry changing the examples or user email to see how the LLM adapts to new tones or edge cases!")
