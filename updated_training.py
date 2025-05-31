import numpy as np
import matplotlib.pyplot as plt
import os

def q_table_training():
    # define environment
    # empty square = 0, O = 1, X = 2. 
    # indexed as an integer base 3 of length 9, running from top left to bottom right
    # eg. 100212001 is a diagonal downwards win for O
    retraining = False
    if os.path.exists("q_table_1.npy"):
        print("continuing training q-tables")
        q_values_1 = np.load("q_table_1.npy")
        q_values_2 = np.load("q_table_2.npy")
        retraining = True
    else:
        print("training new q-tables")
        q_values_1 = np.random.uniform(low=-0.01, high=0.01, size=(3 ** 9, 9))
        q_values_2 = np.random.uniform(low=-0.01, high=0.01, size=(3 ** 9, 9))
    # to load and keep training, q_values_1 = np.load("q_table_player1.npy")
     
    # keep track of win history for graph
    win_history_1 = []
    win_history_2 = []
    
    # training values stage 1:
    training_variables = {
        "epsilon": 0.9,
        "epsilon_decay": 0.9995,
        "epsilon_min": 0.3, 
        "discount_factor": 0.98,
        "learning_rate": 0.3,
    }
  
    
    # ai first plays against random moving player
    for episode in range(5000):
    
        # for each player
        for player in [1, 2]:
            opponent = switch_player(player)

            # run the game, and get the state-action pairs for the game
            winner, board_history, move_history = run_random_game(player, training_variables, q_values_1, q_values_2)


            # give rewards
            update_q_tables(winner, board_history, move_history, player, training_variables, q_values_1, q_values_2)

            # update win_history
            if player == 1:
                win_history_1.append(winner)
            else:
                win_history_2.append(winner)

        # decay epsilon and learning rate
        training_variables["epsilon"] = max(training_variables["epsilon"] * training_variables["epsilon_decay"], training_variables["epsilon_min"])
        
        # print epsilon every 500 episodes
        if training_variables["epsilon"] % 1000 == 0:
            print(f"epsilon at episode {episode} = {training_variables["epsilon"]}")




    # training values stage 2:
    training_variables = {
        "epsilon": 0.3,
        "epsilon_decay": 0.9998,
        "epsilon_min": 0.01, 
        "discount_factor": 0.98,
        "learning_rate": 0.1,
    }
   

    # ai then plays against algorithm player
    for episode in range(10000):
    
        # for each player
        for player in [1, 2]:
            opponent = switch_player(player)

            # run the game, and get the state-action pairs for the game
            winner, board_history, move_history = run_blockwin_game(player, training_variables, q_values_1, q_values_2)


            # give rewards
            update_q_tables(winner, board_history, move_history, player, training_variables, q_values_1, q_values_2)

            # update win_history
            if player == 1:
                win_history_1.append(winner)
            else:
                win_history_2.append(winner)

        # decay epsilon and learning rate
        training_variables["epsilon"] = max(training_variables["epsilon"] * training_variables["epsilon_decay"], training_variables["epsilon_min"])
        
        # print epsilon every 500 episodes
        if training_variables["epsilon"] % 1000 == 0:
            print(f"epsilon at episode {episode} = {training_variables["epsilon"]}")

    # save q-table
    np.save("q_table_1.npy", q_values_1)
    np.save("q_table_2.npy", q_values_2)
    # plot the graph of win rate vs episode for both players
    plot_graph(win_history_1, win_history_2)
        



# game_functions
def run_random_game(symbol, training_variables, q_values_1, q_values_2):
    # initialize board state
    board = '000000000'

    move_history = []
    board_history = [board]
    opponent = switch_player(symbol)

    # playing the game (1 loop is 1 pair of moves)
    while True:
        # check if game has ended
        winner = check_winner(board)
        if winner is not None:
            break

        '''OPPONENT MAKES THEIR MOVE'''
        # if player = 2, first move is randomly generated
        if symbol == 1 and move_history == []:
            pass
        else:
            random_move = get_random_move(board)
            board = get_new_board(board, random_move, opponent)
            # update history lists
            board_history.append(board)
            move_history.append(10)

        winner = check_winner(board)
        if winner is not None:
            break


        '''AI MAKES ITS MOVE'''
        # get new action based on the canonicalised board board
        action = get_next_action(training_variables["epsilon"], board, symbol, q_values_1, q_values_2)

        # ai makes its move
        board = get_new_board(board, action, symbol)

        # update history lists
        move_history.append(action)
        board_history.append(board)


    # when game is over, return lists of state-action pairs
    return winner, board_history, move_history

def run_blockwin_game(symbol, training_variables, q_values_1, q_values_2):
    # initialize board state
    board = '000000000'

    move_history = []
    board_history = [board]
    opponent = switch_player(symbol)

    # playing the game (1 loop is 1 pair of moves)
    while True:
        # check if game has ended
        winner = check_winner(board)
        if winner is not None:
            break

        '''OPPONENT MAKES THEIR MOVE'''
        # if player = 2, first move is randomly generated
        if symbol == 1 and move_history == []:
            pass
        else:
            opponent_move = get_BW_move(board, symbol)
            board = get_new_board(board, opponent_move, opponent)
            # update history lists
            board_history.append(board)
            move_history.append(10)

        winner = check_winner(board)
        if winner is not None:
            break


        '''AI MAKES ITS MOVE'''
        # get new action based on the canonicalised board board
        action = get_next_action(training_variables["epsilon"], board, symbol, q_values_1, q_values_2)

        # ai makes its move
        board = get_new_board(board, action, symbol)

        # update history lists
        move_history.append(action)
        board_history.append(board)


    # when game is over, return lists of state-action pairs
    return winner, board_history, move_history





# useful functions

def line_of_two(board, move, player):
    lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [6, 4, 2]]
    for line in lines:
        player_count = 0
        space_count = 0
        for item in line:
            if board[item] == str(player):
                player_count += 1
            elif board[item] == '0':
                space_count += 1
        if player_count == 2 and space_count == 1 and move in line:
            return True
    return False
    

def blocked_line(board, move, player):
    opponent = switch_player(player)
    lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [6, 4, 2]]
    for line in lines:
        if move not in line:
            continue
        opponent_count = 0
        player_count = 0 
        for item in line:
            if board[item] == str(opponent):
                opponent_count += 1
            elif board[item] == str(player):
                player_count += 1
        if player_count == 1 and opponent_count == 2:
            return True
    return False



def update_q_tables(winner, board_history, move_history, player, variables, q_values_1, q_values_2):
    opponent = switch_player(player)
    # work backwards from final move
    for t in reversed(range(len(move_history))):
        # skip the random players moves
        if move_history[t] == 10:
            continue
        board, move = board_history[t], move_history[t]
        
        # get standard board and move combo
        board_std, transform = convert_board_standard(board)
        state = int(board_std, 3)
        action = convert_move(move, transform)

    
        # if terminal move, give full rewards
        if t == len(move_history) - 1 or t == len(move_history) - 2:
            reward = 0
            if winner == player:
                reward += 1
            elif winner == opponent:
                reward -= 1
            target = reward

        else:
            # non-terminal state, q_value = reward + discount_factor * max_future_q
            next_board_std, transform = convert_board_standard(board_history[t+2])
            next_state = int(next_board_std, 3)
            
            # calculate max_future_q
            valid_next_moves = [i for i, c in enumerate(next_board_std) if c == '0']
            if player == 1:
                max_future_q = np.max(q_values_1[next_state]) if valid_next_moves else 0
            else:
                max_future_q = np.max(q_values_2[next_state]) if valid_next_moves else 0
            # non-terminal state, immediate reward = 0
            target = 0 + variables["discount_factor"] * max_future_q

        # calculate and update new q-value
        if player == 1:
            q_values_1[state, action] += variables["learning_rate"] * (target - q_values_1[state, action])
            new_q = q_values_1[state, action]
        else:
            q_values_2[state, action] += variables["learning_rate"] * (target - q_values_2[state, action])
            new_q = q_values_2[state, action]

def get_BW_move(board, player):
    opponent = switch_player(player)

    alpha = np.random.random()
    if alpha < 0.1:
        random_move = get_next_action( 1, board, player, [1], [1])
        return random_move


    # if player has 2 in a row, block. if opponent has 2 in a row, win
    lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [6, 4, 2]]
    for line in lines:
        opponent_count = 0
        space_count = 0
        space = None
        for item in line:
            if board[item] == str(opponent):
                opponent_count += 1
            elif board[item] == '0':
                space_count += 1
                space = item
        if opponent_count == 2 and space_count == 1:
            return space
    for line in lines:
        player_count = 0
        space_count = 0
        space = None
        for item in line:
            if board[item] == str(player):
                player_count += 1
            elif board[item] == '0':
                space_count += 1
                space = item
        if player_count == 2 and space_count == 1:
            return space
    
    # else pick random move
    random_move = random_move = get_next_action( 1, board, player, [1], [1])
    return random_move

def check_winner(board):
    if board[0] == board[1] == board[2] and board[0] != '0':
        return int(board[0])
    elif board[3] == board[4] == board[5] and board[3] != '0':
        return int(board[3])
    elif board[6] == board[7] == board[8] and board[6] != '0':
        return int(board[6])
    elif board[0] == board[3] == board[6] and board[0] != '0':
        return int(board[0])
    elif board[1] == board[4] == board[7] and board[1] != '0':
        return int(board[1])
    elif board[2] == board[5] == board[8] and board[2] != '0':
        return int(board[2])
    elif board[0] == board[4] == board[8] and board[0] != '0':
        return int(board[0])
    elif board[2] == board[4] == board[6] and board[2] != '0':
        return int(board[2])
    elif '0' not in board:
        return 0
    else:
        return None

def get_next_action(epsilon, board, player, q_values_1, q_values_2):
    # if randomly chosen number > epsilon, choose good move
    valid_moves = [] 
    for i, square in enumerate(board):
        if square == '0':
            valid_moves.append(i)
    # convert board to standard rotation
    if np.random.random() > epsilon:
        board_std, transform = convert_board_standard(board)
        state = int(board_std, 3)
        # lookup best move from q-table
        if player == 1:
            q_vals = q_values_1[state].copy()
        else:
            q_vals = q_values_2[state].copy()
        # mask invalid moves
        for i in range(9):
            if i not in valid_moves:
                q_vals[i] = -np.inf
        move = inverse_transform(np.argmax(q_vals), transform)
        return move
    
    else:
        # choose random VALID action
        return np.random.choice(valid_moves)



def get_random_move(board):
    valid_moves = [] 
    for i, square in enumerate(board):
        if square == '0':
            valid_moves.append(i)
    return np.random.choice(valid_moves)

def get_new_board(board, move, player):
    # convert to list to update, then back to string
    board_list = list(board)
    board_list[move] = str(player)
    return "".join(board_list)

def convert_board_standard(board):
    # turn the string into a 3x3 array
    board = np.array(list(board)).reshape(3, 3)
    # get all the symmetries for the board
    # transform in form (rotation count, flip type)
    symmetries = [
        (board, (0, None)), 
        (np.rot90(board, 1), (1, None)),
        (np.rot90(board, 2), (2, None)),
        (np.rot90(board, 3), (3, None)),
        (np.fliplr(board), (0, "lr")),
        (np.flipud(board), (0, "ud")),
        (np.rot90(np.fliplr(board)), (1, "lr")),
        (np.rot90(np.flipud(board)), (1, "ud"))
    ]
    # get "smallest" board from all the symmetries
    min_board = None
    best_transform = None

    for transformed_board, transform in symmetries:
        board_str = "".join(transformed_board.flatten())
        if min_board is None or board_str < min_board:
            min_board = board_str
            best_transform = transform
    return min_board, best_transform

def convert_move(move, transform):
    x, y = move % 3, move // 3
    rot, flip = transform
    # rotation first
    for _ in range(rot):
        x, y = y, 2 - x
    # inverse flip
    if flip == "lr":
        x = 2 - x
    elif flip == "ud":
        y = 2 - y
    return (y * 3) + x
        

def inverse_transform(move, transform):
    x, y = move % 3, move // 3
    rot, flip = transform
    # inverse flip first
    if flip == "lr":
        x = 2 - x
    elif flip == "ud":
        y = 2 - y
    # inverse rotation
    for _ in range(rot):
        x, y = 2 - y, x
    return (y * 3) + x

def switch_player(player):
    if player == 1:
        player = 2
    else:
        player = 1
    return player

    

def plot_graph(win_history_1, win_history_2):
    # format win_histories to the same size
    min_size = min(len(win_history_1), len(win_history_2))
    h1 = np.array(win_history_1[:min_size])
    h2 = np.array(win_history_2[:min_size])

    # get rolling average windows
    window_size = 500
    win_rate_player1 = np.convolve(h1 == 1, np.ones(window_size), 'valid') / window_size 
    win_rate_player2 = np.convolve(h2 == 2, np.ones(window_size), 'valid') / window_size
    draw_rate_player1 = np.convolve(h1 == 0, np.ones(window_size), 'valid') / window_size
    draw_rate_player2 = np.convolve(h2 == 0, np.ones(window_size), 'valid') / window_size
    
    # episodes corresponding to rolling window
    episodes = np.arange(window_size, len(win_history_1) + 1)

    # plot graph
    plt.figure(figsize=(10, 5))
    plt.plot(episodes, win_rate_player1, label="Win rate playing as O")
    plt.plot(episodes, win_rate_player2, label="Win rate playing as X")
    plt.plot(episodes, draw_rate_player1, label="Draw rate playing as O")
    plt.plot(episodes, draw_rate_player2, label="Draw rate playing as X")
    plt.xlabel("Episode")
    plt.ylabel("Win rate")
    plt.title("Rolling Win Rate vs Episode")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    q_table_training()






'''
first stage: against random opponents
    small number of episodes
    heavily reward intermediate stages (line of 2 = 0.1, block = 0.2)
    high exploration, epsilon = 0.5 - 1
    
second stage: against blocking and winning bot
    for long time
    occassional random moves to disrupt patterns
    aims to punish ai mistakes
    medium exploration, epsilon = 0.1 - 0.4

third stage: self play 
    small number of episodes
    only reward both players after a game
    low exploration for strategy refinement, epsilon = 0.05

    
default training variables:
    epsilon = 0.99
    epsilon_decay = 0.996
    epsilon_min = 0.05
    learning_rate = 0.2
    discount_factor = 0.98

'''