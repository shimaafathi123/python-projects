import tkinter as tk
import random

def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "It's a tie!"

    if player_choice == 'rock':
        if computer_choice == 'paper':
            return 'Computer wins!'
        else:
            return 'Player wins!'
    elif player_choice == 'paper':
        if computer_choice == 'scissors':
            return 'Computer wins!'
        else:
            return 'Player wins!'
    elif player_choice == 'scissors':
        if computer_choice == 'rock':
            return 'Computer wins!'
        else:
            return 'Player wins!'

def play_game(player_choice):
    choices = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(choices)
    winner = determine_winner(player_choice, computer_choice)
    show_result(winner)

def on_rock():
    play_game('rock')

def on_paper():
    play_game('paper')

def on_scissors():
    play_game('scissors')

def show_result(winner):
    result_window = tk.Toplevel(root)
    result_window.title('Result')
    result_window.geometry('200x100')
    result_window.configure(bg='#ffffff')

    result_label = tk.Label(result_window, text=winner, bg='#ffffff', font=('Helvetica', 12))
    result_label.pack(pady=20)

root = tk.Tk()
root.title('Rock, Paper, Scissors')

# Styling
root.geometry('300x200')
root.configure(bg='#f0f0f0')


rock_button = tk.Button(root, text='Rock', command=on_rock, bg='#ff9999', fg='white', font=('Helvetica', 12))
rock_button.pack(pady=5, padx=10, side=tk.LEFT)

paper_button = tk.Button(root, text='Paper', command=on_paper, bg='#99ff99', fg='white', font=('Helvetica', 12))
paper_button.pack(pady=5, padx=10, side=tk.LEFT)

scissors_button = tk.Button(root, text='Scissors', command=on_scissors, bg='#9999ff', fg='white', font=('Helvetica', 12))
scissors_button.pack(pady=5, padx=10, side=tk.LEFT)

root.mainloop()
