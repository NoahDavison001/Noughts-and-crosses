import sys
from tkinter import *
from tkinter import ttk
from alg_player import get_best_move
import numpy as np
from updated_training import convert_board_standard, inverse_transform, convert_move




def main():
    # main window setup
    window = Tk()
    window.title("Noughts and Crosses")
    window.geometry("400x400")
    window.resizable(width=False, height=False)
    window.protocol("WM_DELETE_WINDOW", lambda: on_close(window, sys))

    # setup state variable
    state = initialize_state()

    # show first menu
    show_menu(window, state)

    window.mainloop()



def initialize_state():
    state = {
        "board": [["", "", ""], ["", "", ""], ["", "", ""]],
        "buttons": [[None for _ in range(3)] for _ in range(3)],
        "current_player": None,
        "menuframe": None,
        "gameboard": None,
        "turn_label": None,
        "game_end": False,
        "alg_mode": False,
        "AI_mode": False,
        "playing_as": 'x',
        "q_values_1": None,
        "q_values_2": None,
        }
    return state
    

def show_menu(window, state):
    # clear menu
    if state["gameboard"]:
        state["gameboard"] = None

    # reset mode variables
    state = initialize_state()

    # create frame widget
    if not window.winfo_exists():
        return
    state["menuframe"] = Frame(window, bg='lightblue')
    state["menuframe"].grid(column=0, row=0, sticky=(N, W, E, S))
    state["menuframe"].columnconfigure(0, weight=1)

    # put widgets inside frame
    state["playing_as"] = StringVar(value='x')
    spacing = 75
    Label(state["menuframe"], text="Main Menu", font="none 18 bold", bg='lightblue').grid(column=0, row=0, sticky=(EW), padx=135, pady=(30, 64))
    Radiobutton(state["menuframe"], text="Play as O", variable=state["playing_as"], value="x", bg='lightblue').place(x=150, y=92, anchor="center")
    Radiobutton(state["menuframe"], text="Play as X", variable=state["playing_as"], value="o", bg='lightblue').place(x=256, y=92, anchor="center")
    Label(state["menuframe"], text="Select an opponent:", font="none 12", bg='lightblue').grid(column=0, row=1, sticky=(EW), padx=135, pady=(0, 20))
    ttk.Button(state["menuframe"], text="VS human", command=lambda: start_game(window, state)).grid(column=0, row=2, sticky=(EW), pady=(0, 30), padx=spacing)
    ttk.Button(state["menuframe"], text="VS algorithm", command=lambda: start_alg_game(window, state)).grid(column=0, row=3, sticky=(EW), pady=(0, 30), padx=spacing)
    ttk.Button(state["menuframe"], text="VS MLA", command=lambda: start_ai_game(window, state)).grid(column=0, row=4, sticky=(EW), padx=spacing, pady=(0, 30))
    ttk.Button(state["menuframe"], text="Exit", command=window.destroy).grid(column=0, row=5, sticky=(), pady=(0, 40))

    



    
def start_game(window, state):
    # clear window
    state["menuframe"].destroy()

    # load game board
    if not window.winfo_exists():
        return
    state["gameboard"] = Frame(window, bg='lightblue', width=400, height=400)
    state["gameboard"].grid(column=0, row=0, sticky=(N, W, E, S))  
    state["gameboard"].grid_propagate(False)
    
    # reset state variables
    state["current_player"] = "o"
    state["board"] = [["p", "p", "p"], ["p", "p", "p"], ["p", "p", "p"]]
    state["end_game"] = False

    # put widgets on board

    # if playing against algorithm
    if state["alg_mode"]:
        # alter layout
        Label(state["gameboard"], text="VS algorithm", font="none 14", bg='lightblue').place(x=200, y=15, anchor="center")
        for row in range(3):
            for col in range(3):
                def make_cmd(y=row, x=col):
                    return lambda: player_move(x, y, state, window)
                state["buttons"][row][col] = Button(state["gameboard"], text="", command=make_cmd(), font="none 18", width=1, height=1)
                state["buttons"][row][col].place(x=(55 + col*110), y=(40 + row*100), width=90, height=90)
    
        state["turn_label"] = Label(state["gameboard"], text=f"Player {state["current_player"].upper()} turn", font="none 14", bg='lightblue')
        state["turn_label"].place(x=200, y=345, anchor="n")

    
    # if playing against ai
    elif state["AI_mode"]:
        # alter layout
        Label(state["gameboard"], text="VS Q-learning algorithm", font="none 14", bg='lightblue').place(x=200, y=15, anchor="center")
        for row in range(3):
            for col in range(3):
                def make_cmd(y=row, x=col):
                    return lambda: player_move_ai(x, y, state, window)
                state["buttons"][row][col] = Button(state["gameboard"], text="", command=make_cmd(), font="none 18", width=1, height=1)
                state["buttons"][row][col].place(x=(55 + col*110), y=(40 + row*100), width=90, height=90)
    
        state["turn_label"] = Label(state["gameboard"], text=f"Player {state["current_player"].upper()} turn", font="none 14", bg='lightblue')
        state["turn_label"].place(x=200, y=345, anchor="n")

            
            
    # if playing default mode
    else:
        Label(state["gameboard"], text="VS human", font="none 14", bg='lightblue').place(x=200, y=15, anchor="center")
        for row in range(3):
            for col in range(3):
                def make_cmd(y=row, x=col):
                    return lambda: make_move(x, y, state, window)
                state["buttons"][row][col] = Button(state["gameboard"], text="", command=make_cmd(), font="none 18", width=1, height=1)
                state["buttons"][row][col].place(x=(55 + col*110), y=(40 + row*100), width=90, height=90)
        
        state["turn_label"] = Label(state["gameboard"], text=f"Player {state["current_player"].upper()} turn", font="none 14", bg='lightblue')
        state["turn_label"].place(x=200, y=345, anchor="n")

    


def start_alg_game(window, state):
    # set game mode
    state["alg_mode"] = True
    start_game(window, state)

    # algorithm makes first move if going first
    if state["playing_as"].get() == 'o':
        alg_move = get_best_move(state)
        make_move(alg_move[0], alg_move[1], state, window)
        print("tried")


def start_ai_game(window, state):
    # set game mode
    state["AI_mode"] = True

    # load q table for each player
    state["q_values_1"], state["q_values_2"] = load_q_tables()

    start_game(window, state)

    # algorithm makes first move if going first
    if state["playing_as"].get() == 'o':
        ai_move = get_ai_action('000000000', 1, state)
        make_move(ai_move % 3, ai_move // 3, state, window)
        print(f"ai move {ai_move}")



def make_move(x, y, state, window):
    # update gameboard
    state["buttons"][int(y)][int(x)].config(text=state["current_player"].upper(), state='disabled')
    state["board"][int(y)][int(x)] = state["current_player"]

    # check for win or draw
    winner = check_winner(state)
    draw = check_draw(state)
    if winner:
        print("winner")
        end_game(winner, state, window)
        return
    elif draw:
        print("draw")
        end_game(winner, state, window)
        return

    # switch turn to other player
    if state["current_player"] == 'x':
        state["current_player"] = 'o'
    else:
        state["current_player"] = 'x'
    state["turn_label"].config(text=f"Player {state["current_player"].upper()} turn")





def player_move(x, y, state, window):
    make_move(x, y, state, window)
    if not state["game_end"]:
        alg_move = get_best_move(state)
        make_move(alg_move[0], alg_move[1], state, window)



def player_move_ai(x, y, state, window):
    make_move(x, y, state, window)
    # write board into ai notation
    board = ''
    for row in state["board"]:
        for col in row:
            if col == 'p':
                board += '0'
            elif col == 'o':
                board += '1'
            else:
                board += '2'
    print(board, "board")
            
    # determine current player
    ai = 1 if state["playing_as"].get() == 'o' else 2

    # do ai move
    if not state["game_end"]:
        ai_move = get_ai_action(board, ai, state)
        print(f"ai move {ai_move}")
        make_move(ai_move % 3, ai_move // 3, state, window)


        



def get_ai_action(board, player, state):
    # CONVERT BOARD FIRST

    valid_moves = [] 
    for i, square in enumerate(board):
        if square == '0':
            valid_moves.append(i)

    # convert board to standard rotation
    board_std, transform = convert_board_standard(board)
    board_state = int(board_std, 3)
    valid_moves_std = [convert_move(move, transform) for move in valid_moves]
    # lookup best move from q-table
    if player == 1:
        q_vals = state["q_values_1"][board_state].copy()
    else:
        q_vals = state["q_values_2"][board_state].copy()
    # mask invalid moves
    for i in range(9):
        if i not in valid_moves_std:
            q_vals[i] = -np.inf
    move = inverse_transform(np.argmax(q_vals), transform)
    return move
    

def check_winner(state):
    # horizontal line
    for row in state["board"]:
        if len(set(row)) == 1 and row[0] != 'p':
            return True
    
    # vertical line
    for i in range(3):
        col = []
        for j in range(3):
            col.append(state["board"][j][i]) 
        if len(set(col)) == 1 and col[0] != 'p':
            return True
        
    # diagonal lines
    up_diag = []
    down_diag = []
    for i in range(3):
        up_diag.append(state["board"][2-i][i])
        down_diag.append(state["board"][i][i])
    if (len(set(up_diag)) == 1 or len(set(down_diag)) == 1) and up_diag[1] != 'p':
        return True
    
    # if no winner, return false
    return False
        


def load_q_tables():
    try:
        q_table_1 = np.load("q_table_1.npy")
        q_table_2 = np.load("q_table_2.npy") 
        print("Q-tables loaded successfully!")
        return q_table_1, q_table_2
    except FileNotFoundError:
        print("Error: Could not find q_table_1.npy or q_table_2.npy")
        print("Make sure both files are in the current directory.")
        return None, None


def check_draw(state):
    # go through board
    for row in state["board"]:
        for col in row:
            # check for blank squares
            if col == "p":
                return False
    
    # if no blank squares and no winner, must be a draw
    return True
    




def end_game(winner, state, window):
    # update label below grid to tell players who wins
    if winner:
        state["turn_label"].config(text=f"Player {state["current_player"]} wins!")
    else:
        state["turn_label"].config(text="Draw!")
    state["game_end"] = True
    # leave message up for 2 seconds, then return to main menu
    window.after(2000, lambda: show_menu(window, state))


def on_close(window, sys):
    window.destroy()
    sys.exit()

if __name__ == "__main__":
    main()
