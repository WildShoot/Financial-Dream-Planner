import os
import ollama


KNOWLEDGE_FOLDER = "knowledge_base"


def search_knowledge(question):

    question = question.lower()

    selected_file = None


    # Select relevant file
    if "investment" in question:
        selected_file = "investment_categories.txt"

    elif "shortfall" in question or "saving" in question:
        selected_file = "financial_guidelines.txt"

    elif "goal" in question:
        selected_file = "goal_planning_rules.txt"

    else:
        return {
            "answer": "Sorry, information is not available.",
            "source": None
        }


    # Create file path
    file_path = os.path.join(
        KNOWLEDGE_FOLDER,
        selected_file
    )


    # Read knowledge file
    with open(file_path, "r", encoding="utf-8") as file:
        context = file.read()


    # Create prompt
    prompt = f"""
You are a helpful financial assistant.

Use the information below to answer the user's question.

Do not copy the information exactly.
Give a simple, clear and useful answer.

Information:
{context}

User Question:
{question}
"""


    # Send question to Ollama
    response = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    # Return generated answer
    return {
        "answer": response["message"]["content"],
        "source": selected_file
    }