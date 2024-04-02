import time

# Typewritter Effect
def typewrite_alpha(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # Print newline after completing the text

# Typewritter Effect
def typewrite_beta(prefix, text, delay=0.05):
    print(prefix, end='', flush=True)  # Print the prefix normally
    for char in text:
        print(char, end='', flush=True)  # Print each character of the text with the typewriter effect
        time.sleep(delay)
    print()  # Add a newline after printing the text

# Example usage
typewrite_alpha("Hi!!! I'm Iris")
typewrite_beta("Iris: ", "Hi!!! I'm Iris")