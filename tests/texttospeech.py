import pyttsx3
# Initialize the TTS engine
engine = pyttsx3.init()

# Set properties (adjust rate as desired)
engine.setProperty("rate", 150)  # Adjust speed (default is 200, lower values decrease speed)

# Set the voice (you can experiment with different voices to achieve desired pitch)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[2].id)  # Use the first available voice (0-3)

# Say something
engine.say("You pathetic human")

# Wait for speech to finish
engine.runAndWait()
