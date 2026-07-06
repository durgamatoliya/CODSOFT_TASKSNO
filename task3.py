import tkinter as tk
from tkinter import messagebox
import math

# =====================================================================
# 1. THE GAME MECHANICS & MINIMAX AI ENGINE
# =====================================================================
def check_winner(board):
    """Checks the current board array state. Returns 'O', 'X', 'Draw', or None."""
    # Define all 8 possible winning line configurations
    win_states = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    
    for line in win_states:
        if board[line[0]] == board[line[1]] == board[line[2]] and board[line[0]] != "":
            return board[line[0]]
            
    if "" not in board:
        return "Draw"
        
    return None

def minimax(board, is_maximizing):
    """Adversarial recursive search tracking optimal outcomes."""
    # Base Case: Evaluate the terminal leaf nodes
    result = check_winner(board)
    if result == "O": return 10
    if result == "X": return -10
    if result == "Draw": return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = "O"  # Simulated move
                score = minimax(board, False)
                board[i] = ""   # Undo simulated move
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = "X"  # Simulated move
                score = minimax(board, True)
                board[i] = ""   # Undo simulated move
                best_score = min(score, best_score)
        return best_score

def find_best_move(board):
    """Evaluates all legal moves via Minimax and selects the absolute best index."""
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

# =====================================================================
# 2. INTERACTION MANAGERS & GUI CONTROLS
# =====================================================================
def on_click(index):
    """Handles human move actions, updates states, and prompts the AI turn sequence."""
    global current_player
    
    if board_state[index] == "" and current_player == "Human":
        # 1. Apply Human Move
        board_state[index] = "X"
        buttons[index].config(text="X", fg="#f43f5e", disabledforeground="#f43f5e", state="disabled")
        
        if evaluate_game_end():
            return
            
        # 2. Shift state control directly over to AI Player
        current_player = "AI"
        status_label.config(text="AI is calculating...", fg="#38bdf8")
        root.after(400, trigger_ai_move) # 400ms delay makes the AI feel more natural

def trigger_ai_move():
    """Calculates unbeatable move vectors and applies changes into grid arrays."""
    global current_player
    
    ai_index = find_best_move(board_state)
    if ai_index != -1:
        board_state[ai_index] = "O"
        buttons[ai_index].config(text="O", fg="#38bdf8", disabledforeground="#38bdf8", state="disabled")
        
    if evaluate_game_end():
        return
        
    current_player = "Human"
    status_label.config(text="Your Turn (Player X)", fg="#f43f5e")

def evaluate_game_end():
    """Checks board resolutions and alerts conclusions visually on screen."""
    winner = check_winner(board_state)
    if winner:
        if winner == "Draw":
            status_label.config(text="It's a Draw!", fg="#a1a1aa")
            messagebox.showinfo("Game Over", "Well played! It's a draw.")
        elif winner == "O":
            status_label.config(text="AI Wins!", fg="#38bdf8")
            messagebox.showinfo("Game Over", "The AI wins! Minimax is mathematically unbeatable.")
        else:
            status_label.config(text="You Win!", fg="#4ade80")
            messagebox.showinfo("Game Over", "Impossible! You won?")
        reset_game()
        return True
    return False

def reset_game():
    """Wipes active configurations clean for successive rounds."""
    global board_state, current_player
    board_state = [""] * 9
    current_player = "Human"
    status_label.config(text="Your Turn (Player X)", fg="#f43f5e")
    for btn in buttons:
        btn.config(text="", state="normal", bg="#27272a")

# =====================================================================
# 3. GRAPHICAL GRID VIEW ASSEMBLY
# =====================================================================
root = tk.Tk()
root.title("Unbeatable Tic-Tac-Toe AI")
root.geometry("400x500")
root.configure(bg="#1e1e24")

# Global tracking arrays
board_state = [""] * 9
current_player = "Human"
buttons = []

# Title Label Banner
title_label = tk.Label(root, text="NEURAL TIC-TAC-TOE", font=("Helvetica", 16, "bold"), bg="#1e1e24", fg="#f5f5f7")
title_label.pack(pady=15)

# Status Turn Label Display
status_label = tk.Label(root, text="Your Turn (Player X)", font=("Helvetica", 12, "bold"), bg="#1e1e24", fg="#f43f5e")
status_label.pack(pady=5)

# Game Matrix Board Grid Container Layout
grid_frame = tk.Frame(root, bg="#1e1e24")
grid_frame.pack(pady=10)

# Build out the 3x3 interactive game matrix elements layout configurations
for i in range(9):
    btn = tk.Button(
        grid_frame,
        text="",
        font=("Helvetica", 24, "bold"),
        width=4,
        height=1,
        bg="#27272a",
        activebackground="#3f3f46",
        borderwidth=2,
        relief="solid",
        command=lambda idx=i: on_click(idx)
    )
    # Map elements across coordinate boundaries dynamically
    row = i // 3
    col = i % 3
    btn.grid(row=row, column=col, padx=6, pady=6)
    buttons.append(btn)

# Operational Control Action Frame Elements Layout Configuration
btn_reset = tk.Button(
    root, 
    text="Restart Matrix", 
    font=("Helvetica", 10, "bold"), 
    bg="#3f3f46", 
    fg="#ffffff", 
    activebackground="#52525b",
    padx=15, 
    pady=6, 
    borderwidth=0, 
    command=reset_game
)
btn_reset.pack(pady=20)

root.mainloop()
