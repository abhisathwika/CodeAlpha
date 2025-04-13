import nltk
import random
import string
from nltk.chat.util import Chat, reflections
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Initialize the lemmatizer
lemmer = WordNetLemmatizer()

# Function to lemmatize tokens
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

# Remove punctuation
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

# Normalize the user input (lowercase, no punctuation, lemmatized)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Memory for the chatbot
user_name = ""

# Expanded response function
def chatbot_response(user_input):
    global user_name
    user_input = user_input.lower()

    # Exit phrases
    if user_input in ["bye", "exit", "quit"]:
        return "Goodbye! Have a great day!"

    # Greetings
    elif user_input in ["hi", "hello", "hey"]:
        return random.choice(["Hello!", "Hi there!", "Hey! How can I assist you today?"])

    # Asking for bot name
    elif "your name" in user_input:
        return "I am your friendly chatbot, created using NLTK."

    # Asking user’s name
    elif "my name is" in user_input:
        user_name = user_input.split("is")[-1].strip().capitalize()
        return f"Nice to meet you, {user_name}!"

    elif "who am i" in user_input:
        return f"You're {user_name}!" if user_name else "I don't know your name yet. Tell me by saying 'My name is ...'"

    # Asking about bot's health
    elif "how are you" in user_input:
        return random.choice([
            "I'm doing well, thanks for asking!",
            "I'm just a bunch of code, but feeling great!",
            "All systems functional! How about you?"
        ])

    # Asking for help
    elif "help" in user_input or "what can you do" in user_input:
        return ("I can chat with you, remember your name, and respond to some questions. "
                "Try saying things like 'How are you?', 'What is your name?', or 'Tell me a joke'.")

    # Jokes
    elif "joke" in user_input:
        return random.choice([
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don’t skeletons fight each other? They don’t have the guts.",
            "I'm reading a book on anti-gravity. It's impossible to put down!"
        ])

    # Thank you
    elif "thank" in user_input:
        return "You're welcome! 😊"

    # Default response
    else:
        return random.choice([
            "I'm not sure I understand. Can you rephrase that?",
            "Interesting... tell me more!",
            "I'm still learning. Ask me something else!"
        ])

# Main chat loop
def chat():
    print("Chatbot: Hello! I'm your chatbot. Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['bye', 'exit', 'quit']:
            print("Chatbot: Goodbye! 👋")
            break
        print("Chatbot:", chatbot_response(user_input))

# Start the chatbot
chat()
