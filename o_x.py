import sys
from tkinter import *
from tkinter import ttk




def main():
    # main window setup
    window = Tk()
    window.title("Noughts and Crosses")
    window.geometry("400x400")
    window.resizable(width=False, height=False)
    window.protocol("WM_DELETE_WINDOW", lambda: on_close(window, sys))

    # setup state variable
    state = {
        "board": [["", "", ""], ["", "", ""], ["", "", ""]],
        "buttons": [[None for _ in range(3)] for _ in range(3)],
        "current_player": None,
        "menuframe": None,
        "gameboard": None,
        "turn_label": None,
        
    }

    # show first menu
    show_menu(window, state)

    window.mainloop()





def show_menu(window, state):
    # clear menu
    if state["gameboard"]:
        state["gameboard"] = None

    # create frame widget
    if not window.winfo_exists():
        return
    state["menuframe"] = Frame(window, bg='lightblue')
    state["menuframe"].grid(column=0, row=0, sticky=(N, W, E, S))
    state["menuframe"].columnconfigure(0, weight=1)

    # put widgets inside frame
    spacing = 75
    Label(state["menuframe"], text="Main Menu", font="none 18 bold", bg='lightblue').grid(column=0, row=0, sticky=(EW), padx=135, pady=(30, 64))
    Label(state["menuframe"], text="Select an opponent:", font="none 12", bg='lightblue').grid(column=0, row=1, sticky=(EW), padx=135, pady=(0, 20))
    ttk.Button(state["menuframe"], text="VS human", command=lambda: start_game(window, state)).grid(column=0, row=2, sticky=(EW), pady=(0, 30), padx=spacing)
    ttk.Button(state["menuframe"], text="VS algorithm").grid(column=0, row=3, sticky=(EW), pady=(0, 30), padx=spacing)
    ttk.Button(state["menuframe"], text="VS MLA").grid(column=0, row=4, sticky=(EW), padx=spacing, pady=(0, 30))
    ttk.Button(state["menuframe"], text="Exit", command=window.destroy).grid(column=0, row=5, sticky=(), pady=(0, 40))

    



    
def start_game(window, state):
    # clear window
    state["menuframe"].grid_forget()

    # load game board
    if not window.winfo_exists():
        return
    state["gameboard"] = Frame(window, bg='lightblue', width=400, height=400)
    state["gameboard"].grid(column=0, row=0, sticky=(N, W, E, S))  
    state["gameboard"].grid_propagate(False)
    
    # reset state variables
    state["current_player"] = "o"
    state["board"] = [["p", "p", "p"], ["p", "p", "p"], ["p", "p", "p"]]

    # put widgets on board
    Label(state["gameboard"], text="VS human", font="none 14", bg='lightblue').place(x=200, y=15, anchor="center")
    for row in range(3):
        for col in range(3):
            def make_cmd(x=row, y=col):
                return lambda: make_move(x, y, state, window)
            state["buttons"][row][col] = Button(state["gameboard"], text="", command=make_cmd(), font="none 18", width=1, height=1)
            state["buttons"][row][col].place(x=(55 + col*110), y=(40 + row*100), width=90, height=90)
    
    state["turn_label"] = Label(state["gameboard"], text=f"Player {state["current_player"]} turn", font="none 14", bg='lightblue')
    state["turn_label"].place(x=200, y=345, anchor="n")

    



def make_move(x, y, state, window):
    # update gameboard
    state["buttons"][x][y].config(text=state["current_player"], state='disabled')
    state["board"][x][y] = state["current_player"]
    print(state["board"])

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
    state["turn_label"].config(text=f"Player {state["current_player"]} turn")

    

    

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
    # leave message up for 2 seconds, then return to main menu
    window.after(2000, lambda: show_menu(window, state))





def on_close(window, sys):
    window.destroy()
    sys.exit()

if __name__ == "__main__":
    main()
