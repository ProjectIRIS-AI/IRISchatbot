import os
import json
import time
from difflib import get_close_matches

# Settings
knowledgebase_folder = "Knowledgebase"
knowledgebase_file = "Iris.json"

bot_prompt = "Iris: "
user_prompt = ">> "
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


# Typewritter Effect
def typewrite(prefix, text, delay=0.05):
    print(prefix, end='', flush=True)  # Print the prefix normally
    for char in text:
        print(char, end='', flush=True)  # Print each character of the text with the typewriter effect
        time.sleep(delay)
    print()  # Add a newline after printing the text


# Main Function
def main():
    knowledge_base: dict = load_knowledge_base(file_path)

    while True:
        user_input: str = input(user_prompt)

        if user_input.lower() == "q":
            break

        if user_input.lower() == "cls":
            os.system("cls")

        best_match: str | None = find_best_match(user_input, [p["prompt"] for p in knowledge_base["prompts"]])

        if best_match:
            response: str = get_response_for_prompt(best_match, knowledge_base)
            typewrite(bot_prompt, response)
        else:
            print(bot_prompt, default_notfound_error)
            new_response: str = input(user_prompt)

            if new_response.lower() != "skip":
                knowledge_base["prompts"].append({"prompt": user_input, "response": new_response})
                save_knowledge_base(file_path, knowledge_base)
                typewrite(bot_prompt, default_iris_thank)


# Run Script
if __name__ == "__main__":
    main()
