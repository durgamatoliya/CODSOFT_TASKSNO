import datetime
import random
import re
import tkinter as tk
from tkinter import scrolledtext


# =====================================================================
# 1. TEXT PREPROCESSING & NATURAL LANGUAGE LOGIC
# =====================================================================
def clean_input(user_text):
    """Normalize text by converting to lowercase and stripping punctuation."""
    user_text = user_text.lower().strip()
    # Remove common punctuation marks using regular expressions
    user_text = re.sub(r"[.,\/#!$%\^&\*;:{}=\-_`~?()]", "", user_text)
    return user_text


def get_bot_response(user_input):
    """Predefined rules using pattern matching (if-elif-else logic)."""
    cleaned = clean_input(user_input)

    # Rule 1: Greetings
    if "hello" in cleaned or "hi" in cleaned or "hey" in cleaned:
        return "Hello there! Ask me for a joke, a tech fact, or the current time!"

    # Rule 2: Tell a Joke
    elif "joke" in cleaned:
        jokes = [
            "Why do programmers wear glasses? Because they can't C#!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
        ]
        return random.choice(jokes)

    # Rule 3: Give the current Date/Time
    elif "time" in cleaned or "date" in cleaned:
        now = datetime.datetime.now()
        return f"Currently, it is {now.strftime('%I:%M %p on %A, %B %d, %Y')}."

    # Rule 4: Fun Tech Facts
    elif "fact" in cleaned or "knowledge" in cleaned:
        facts = [
            "The first computer 'bug' was an actual real moth found trapped in a relay by Grace Hopper in 1947.",
            "The word 'robot' comes from the Czech word 'robota', which means forced labor.",
            "About 92% of the world's currency exists only on computers.",
        ]
        return random.choice(facts)

    # Rule 5: Emotional/Mood responses
    elif "sad" in cleaned or "tired" in cleaned or "bored" in cleaned:
        return (
            "I'm sorry to hear that. Want me to tell you a joke to cheer you up? Just type 'joke'!"
        )
    elif "happy" in cleaned or "good" in cleaned or "great" in cleaned:
        return "Awesome! Glad to hear you're having a good day. What's on your mind?"

    # Rule 6: Identity & Capabilities
    elif "your name" in cleaned or "who are you" in cleaned:
        return "I am RuleBot, your customizable Python desktop assistant!"
    elif "what can you do" in cleaned or "help" in cleaned:
        return "I can tell jokes, share tech facts, look up the time, or just chat. Try asking me!"

    # Rule 7: Farewells
    elif "bye" in cleaned or "goodbye" in cleaned or "exit" in cleaned:
        return "Goodbye! Have a wonderful day!"

    # Default Fallback Rule
    else:
        return "I don't know how to handle that yet. But since I'm open-source, you can add an 'elif' statement to my code to teach me!"


# =====================================================================
# 2. GUI INTERACTION LOGIC
# =====================================================================
def send_message(event=None):
    """Retrieves user text, updates the log, and fetches the bot's response."""
    user_text = user_entry.get().strip()

    # If the input is completely empty, ignore it
    if not user_text:
        return

    # Clear the text box entry right away
    user_entry.delete(0, tk.END)

    # Unlock the chat history widget, append user message, and lock it again
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, f"You: {user_text}\n\n")

    # Fetch response from our rule engine and append it
    bot_response = get_bot_response(user_text)
    chat_window.insert(tk.END, f"🤖 RuleBot: {bot_response}\n\n")

    # Keep screen scrolled to the bottom
    chat_window.see(tk.END)
    chat_window.config(state=tk.DISABLED)


# =====================================================================
# 3. WINDOW SETUP & LAYOUT
# =====================================================================
# Creating the main app frame
root = tk.Tk()
root.title("RuleBot Desktop Dashboard")
root.geometry("450x550")
root.configure(bg="#f0f2f5")

# Scrollable display window for chat logs
chat_window = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 10)
)
chat_window.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

# Greet user immediately upon launch
chat_window.config(state=tk.NORMAL)
chat_window.insert(
    tk.END, "🤖 RuleBot: Hello! Type a message below to start chatting.\n\n"
)
chat_window.config(state=tk.DISABLED)

# Bottom UI panel housing input text boxes and buttons side-by-side
bottom_frame = tk.Frame(root, bg="#f0f2f5")
bottom_frame.pack(padx=15, pady=(0, 15), fill=tk.X)

# Text insertion block for the user
user_entry = tk.Entry(bottom_frame, font=("Arial", 11))
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
user_entry.bind(
    "<Return>", send_message
)  # Enables sending messages just by pressing Enter

# Blue Action Trigger Button
send_button = tk.Button(
    bottom_frame,
    text="Send",
    command=send_message,
    bg="#0084ff",
    fg="white",
    font=("Arial", 10, "bold"),
    relief=tk.FLAT,
    padx=15,
)
send_button.pack(side=tk.RIGHT, padx=(10, 0))

# Execute the application runtime window loop
if __name__ == "__main__":
    root.mainloop()
