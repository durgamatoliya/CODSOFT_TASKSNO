import tkinter as tk
from tkinter import ttk, messagebox

# =====================================================================
# 1. CORE ENGINE & DATASET
# =====================================================================
MOVIE_DATABASE = {
    "The Dark Knight": ["action", "thriller", "crime"],
    "Inception": ["sci-fi", "action", "thriller", "adventure"],
    "Interstellar": ["sci-fi", "drama", "adventure"],
    "The Godfather": ["crime", "drama"],
    "Pulp Fiction": ["crime", "thriller"],
    "Spirited Away": ["animation", "fantasy", "family"],
    "Finding Nemo": ["animation", "comedy", "family", "adventure"],
    "Superbad": ["comedy", "romance"],
    "The Matrix": ["sci-fi", "action"],
    "Gladiator": ["action", "drama", "history"]
}

def generate_recommendations(selected_genres):
    """Calculates similarity scores and returns matching movies."""
    if not selected_genres:
        return []
        
    scores = []
    for movie, genres in MOVIE_DATABASE.items():
        # Count matches between selected genres and movie genres
        matches = sum(1 for g in selected_genres if g in genres)
        if matches > 0:
            score = matches / len(selected_genres)
            scores.append((movie, score, genres))
            
    # Sort by score descending
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

# =====================================================================
# 2. INTERACTION HANDLER
# =====================================================================
def get_selected_genres():
    """Reads checked boxes and updates the recommendation display panel."""
    # Collect all genres that are currently checked
    selected = [genre for genre, var in checkbox_variables.items() if var.get() == 1]
    
    # Clear the previous results from the display box
    result_box.delete("1.0", tk.END)
    
    if not selected:
        result_box.insert(tk.END, "⚠️ Please check at least one category above to get recommendations!")
        return
        
    recommendations = generate_recommendations(selected)
    
    if not recommendations:
        result_box.insert(tk.END, "🤷 No matching movies found for that combination. Try checking other boxes!")
        return
        
    # Format and print the results out nicely in the display box
    result_box.insert(tk.END, f"🌟 Recommendations based on: {', '.join(selected).title()}\n")
    result_box.insert(tk.END, "=" * 60 + "\n\n")
    
    for rank, (movie, score, genres) in enumerate(recommendations, 1):
        match_percentage = int(score * 100)
        genres_string = ", ".join(genres).title()
        
        result_box.insert(tk.END, f"{rank}. {movie}\n")
        result_box.insert(tk.END, f"   🎯 Match Score: {match_percentage}%\n")
        result_box.insert(tk.END, f"   📁 Categories: {genres_string}\n\n")

def reset_selections():
    """Unchecks all boxes and clears the display area."""
    for var in checkbox_variables.values():
        var.set(0)
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, "Select your favorite genres above to discover movies...")

# =====================================================================
# 3. INTERFACE CONSTRUCTION (Tkinter Framework Layout)
# =====================================================================
root = tk.Tk()
root.title("AI Movie Matcher Panel")
root.geometry("520x600")
root.configure(bg="#1e1e24")

# App Header Title Banner
title_label = tk.Label(
    root, 
    text="🎬 MOVIE RECOMMENDATION SYSTEM", 
    font=("Helvetica", 14, "bold"), 
    bg="#1e1e24", 
    fg="#f5f5f7"
)
title_label.pack(pady=15)

# Subheading prompt
prompt_label = tk.Label(
    root, 
    text="What genres are you in the mood for today?", 
    font=("Helvetica", 10, "italic"), 
    bg="#1e1e24", 
    fg="#a1a1aa"
)
prompt_label.pack(pady=2)

# Grid Container Frame for Checkboxes
checkbox_frame = tk.LabelFrame(
    root, 
    text=" Select Categories ", 
    font=("Helvetica", 10, "bold"), 
    bg="#1e1e24", 
    fg="#38bdf8",
    padx=10, 
    pady=10
)
checkbox_frame.pack(padx=20, pady=10, fill=tk.X)

# Collect all unique genres to construct boxes dynamically
unique_genres = sorted(list(set(g for genres in MOVIE_DATABASE.values() for g in genres)))

# Generate tracking variables and layout buttons into grid formation rows
checkbox_variables = {}
columns_limit = 3

for index, genre in enumerate(unique_genres):
    row = index // columns_limit
    col = index % columns_limit
    
    var = tk.IntVar()
    checkbox_variables[genre] = var
    
    chk = tk.Checkbutton(
        checkbox_frame, 
        text=genre.title(), 
        variable=var, 
        command=get_selected_genres, # Triggers real-time live calculations on click!
        bg="#1e1e24", 
        fg="#e4e4e7",
        activebackground="#1e1e24",
        activeforeground="#38bdf8",
        selectcolor="#27272a",
        font=("Helvetica", 10)
    )
    chk.grid(row=row, column=col, sticky="w", padx=15, pady=6)

# Operational Control Action Frame
action_frame = tk.Frame(root, bg="#1e1e24")
action_frame.pack(pady=10)

btn_reset = ttk.Button(action_frame, text="Clear Selections", command=reset_selections)
btn_reset.pack()

# Data Display Text Frame Layout
output_frame = tk.LabelFrame(
    root, 
    text=" Matches Discovered ", 
    font=("Helvetica", 10, "bold"), 
    bg="#1e1e24", 
    fg="#38bdf8",
    padx=10, 
    pady=10
)
output_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# Main Multi-line display textbox module
result_box = tk.Text(
    output_frame, 
    wrap=tk.WORD, 
    font=("Consolas", 10), 
    bg="#111113", 
    fg="#34d399", # Green neon typography out terminal display text layout matrix
    borderwidth=0, 
    padx=8, 
    pady=8
)
result_box.pack(fill=tk.BOTH, expand=True)

# Add initial welcome text inside display window box frame structure area
result_box.insert(tk.END, "Select your favorite genres above to discover movies...")

# Start UI loop sequence handler threads safely inside IDLE
root.mainloop()
