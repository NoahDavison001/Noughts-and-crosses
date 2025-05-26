from random import randint


def get_best_move(state):
    symbol = state["current_player"]
    # list of currently available moves
    free_squares = []
    for y, row in enumerate(state["board"]):
        for x, column in enumerate(row):
            if column == 'p':
                # available
                free_squares.append([x, y])
    print(free_squares)
                

    # if alg can win, win (duh) or block player from winning
    move = check_winning_move(state, symbol)
    if move:
       print("block or win", move)
       return move
    
    # if going first
    if state["going_first"] == True:
        # first move
        if len(free_squares) == 9:
            print("alg says [1, 1]")
            return [1, 1]
        
        # second move
        if len(free_squares) == 7:
            # player takes edge
            for i, row in enumerate(state["board"]):
                # go knights move away from them
                if (i == 0 and row[1] == 'x') or (i == 1 and row[2] == 'x'):
                    print("alg says [0, 2]")
                    return [0, 2]
                elif (i == 1 and row[0] == 'x') or (i == 2 and row[1] == 'x'):
                    print("alg says [2, 0]")
                    return [2, 0]
            # player takes corner
            for i, row in enumerate(state["board"]):
                # go opposite corner
                if i in [0, 2] and row[0] == 'x':
                    print(f"alg says [2, {2-i}]")
                    return [2, 2-i]
                if i in [0, 2] and row[2] == 'x':
                    print(f"alg says [0, {2-i}]")
                    return [0, 2-i]
        
        # third move
        if len(free_squares) == 5:
            # if player takes none-adjacent edge
            # check which corner x took
            x_corner = None
            for i, row in enumerate(state["board"]):
                if i in [0, 2] and row[0] == 'x':
                    if i == 0:
                        x_corner = [0, 0]
                    else:
                        x_corner = [0, 1]
                if i in [0, 2] and row[2] == 'x':
                    if i == 0:
                        x_corner = [2, 0]
                    else:
                        x_corner = [2, 2]

            for i, row in enumerate(state["board"]):
                # find the corner alg played in
                if i == 0 and row[0] == 'o':
                    # check if x nextdoor
                    if state["board"][1][0] == 'x':
                        print("alg says [2, 0]")
                        return [2, 0]
                    elif state["board"][0][1] == 'x':
                        print("alg says [0, 2]")
                        return [0, 2]
                    else:
                        break
                if i == 2 and row[0] == 'o':
                    # check if x nextdoor
                    if state["board"][1][0] == 'x':
                        print("alg says [2, 2]")
                        return [2, 2]
                    elif state["board"][2][1] == 'x':
                        print("alg says [0, 0]")
                        return [0, 0]
                    else:
                        break

                if i == 0 and row[2] == 'o':
                    # check if x nextdoor
                    if state["board"][0][1] == 'x':
                        print("alg says [2, 2]")
                        return [2, 2]
                    elif state["board"][1][2] == 'x':
                        print("alg says [0, 0]")
                        return [0, 0]
                    else:
                        break

                if i == 2 and row[2] == 'o':
                    # check if x nextdoor
                    if state["board"][0][1] == 'x':
                        print("alg says [2, 0]")
                        return [2, 0]
                    elif state["board"][1][0] == 'x':
                        print("alg says [0, 2]")
                        return [0, 2]
                    else:
                        break

    # if going second
    else:
        # first move
        if len(free_squares) == 8:
            # if player went centre
            if state["board"][1][1] == 'o':
                print("alg says [0, 0]")
                return [0, 0]
            # if takes corner
            elif state["board"][0][0] == 'o' or state["board"][2][0] == 'o' or state["board"][0][2] == 'o' or state["board"][2][2] == 'o':
                print("alg says [1, 1]")
                return [1, 1]
            # if takes edge
            elif state["board"][0][1] == 'o' or state["board"][1][0] == 'o':
                print("alg says [0, 0]")
                return [0, 0]
            elif state["board"][1][2] == 'o' or state["board"][2][1] == 'o':
                print("alg says [2, 2]")
                return [2, 2]
        
        # second move
        if len(free_squares) == 6:
            # if player took centre
            if state["board"][1][1] == 'o':
                if state["board"][2][2] == 'o':
                    print("alg says [0, 2]")
                    return [0, 2]
            # if player took corner
            elif state["board"][1][1] == 'x':
                if state["board"][0][0] == 'o':
                    print("alg says [2, 2]")
                    return [2, 2]
                elif state["board"][0][2] == 'o':
                    print("alg says [2, 0]")
                    return [2, 0]
                elif state["board"][2][2] == 'o':
                    print("alg says [0, 0]")
                    return [0, 0]
                elif state["board"][2][0] == 'o':
                    print("alg says [0, 2]")
                    return [0, 2]

    # if no logic move or blocking/winning move, just go random
    random_move = free_squares[randint(0, len(free_squares) - 1)] 
    print(f"random: {random_move}")
    return random_move







def check_winning_move(state, symbol):
    space = []
    # check for rows of 2 and a gap
    for y, row in enumerate(state["board"]):
        if len(set(row)) == 2 and row.count('p') == 1:
            space = [row.index('p'), y]
            if symbol in row:
                return space
            
            
    
    # column check
    for i in range(3):
        col = []
        for j in range(3):
            col.append(state["board"][j][i])
        if len(set(col)) == 2 and col.count('p') == 1:
            space = [i, col.index('p')]
            if symbol in col:
                return space
            
    
    # diagonal check
    up_diag = []
    down_diag = []
    for i in range(3):
        up_diag.append(state["board"][2-i][i])
        down_diag.append(state["board"][i][i])
    for diag in [up_diag, down_diag]:
        if len(set(diag)) == 2 and diag.count('p') == 1:
            if diag == down_diag:
                    space = [diag.index('p'), diag.index('p')]
            else:
                space = [diag.index('p'), 2 - diag.index('p')]
            if symbol in diag:
                return space
        
    # no winning move, return blocking move. if no winning move, return none
    return space


        






'''algorithm layout:
if can win, win
if opponent can win, block

going first:
middle
if player takes edge, go for corner (knight shape from player)
    if player goes corner (block), block their line

if player takes corner, go opposite corner
    if player takes adjacent edge (form line of 2), block
    if player takes non adjacent edge, take corner knights move away
    if player takes corner, block until draw

going second:
if player takes centre, go corner
    if player takes opposite corner (best), go adjacent corner
    block till draw
if player takes edge, take adjacent corner to player
    play random, or block till draw
if player takes corner, go centre
    if player takes opposite corner, go any edge
        block till draw
    
        

else pick random move



'''