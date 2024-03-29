import os
import json
from difflib import get_close_matches

# Settings
knowledgebase_folder = "Knowledgebase"
knowledgebase_file = "Iris.json"
default_notfound_error = "I don't know how to respond. Please teach me or type [SKIP]."
default_iris_thank = "Thank you! I learnt a new thing."


# Knowledge base directory
current_directory = os.getcwd()
file_path = os.path.abspath(os.path.join(current_directory, knowledgebase_folder, knowledgebase_file))


# Load knowledge base
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        data: dict = json.load(file)
    return data


# Save new response to knowledge base
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


# Find prompt that is 60% similar to input
def find_best_match(user_prompt: str, prompts: list[str]) -> str | None:
    matches: list = get_close_matches(user_prompt, prompts, n=1, cutoff=0.6)
    return matches[0] if matches else None


# Get the response for the prompt if found
def get_response_for_prompt(prompt: str, knowledge_base: dict) -> str | None:
    for p in knowledge_base["prompts"]:
        if p["prompt"] == prompt:
            return p["response"]


# Main Function
def main():
    knowledge_base: dict = load_knowledge_base(file_path)

    while True:
        user_input: str = input(">>")

        if user_input.lower() == "quit":
            break

        best_match: str | None = find_best_match(user_input, [p["prompt"] for p in knowledge_base["prompts"]])

        if best_match:
            response: str = get_response_for_prompt(best_match, knowledge_base)
            print(f"Iris: {response}")
        else:
            print(f"Iris: {default_notfound_error}")
            new_response: str = input(">>")

            if new_response.lower() != "skip":
                knowledge_base["prompts"].append({"prompt": user_input, "response": new_response})
                save_knowledge_base(file_path, knowledge_base)
                print(f"Iris: {default_iris_thank}")


# Run Script
if __name__ == "__main__":
    main()
