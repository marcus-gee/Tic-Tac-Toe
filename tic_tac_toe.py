import random
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder


# label encoding for DecisionTreeClassifier inputs
values = list('-ox')
label_encoder = LabelEncoder().fit(values)

# take the dict representation of a board and create a str representation
# used for predictions from the DecisionTreeClassifier
def board_to_str(b):
    s = ''
    for i in range(9):
        c = '-' if b[i] == ' ' else b[i].lower()
        s += c
    return s


# pretty print board for games
def print_board(b):
    def print_numbered(lst):
        # underline number
        under = '\033[4m'
        end   = '\033[0m'
        s = ''
        for num in lst:
            s += under + num + '|' + end + '   |'
        print(s[:-1])

    # top row
    print_numbered(['0', '1', '2'])
    print(f'  {b[0]}  |  {b[1]}  |  {b[2]}  ')

    # middle row
    print('_____|_____|_____')
    print_numbered(['3', '4', '5'])
    print(f'  {b[3]}  |  {b[4]}  |  {b[5]}  ')

    # bottom row
    print('_____|_____|_____')
    print_numbered(['6', '7', '8'])
    print(f'  {b[6]}  |  {b[7]}  |  {b[8]}  ')
    print()


# return the move the computer will play
# the input will be a list of probabilities that the DecisionTreeClassifier
# outputted, which represent the prob that the player's strategy is to play in
# that position. We will use this and typically play in whatever position has
# highest prob. However, if the spot is not playable, we will take the next
# highest. If there are any ties, we pick one of them at random
def get_computer_move(strat, str_board, valid_pos):
    # encode board for predictions
    encoded = label_encoder.transform(list(str_board))
    # probabilities
    s = strat.predict_proba([encoded])[0]
    # tuple of (prob, index) for all valid positions
    options = [(s[int(i)], i) for i in valid_pos]
    # highest prob
    m = max(options, key= lambda x: x[0])[0]
    # return position that is valid w/ highest prob
    return random.choice([k for i, (j, k) in enumerate(options) if j == m])


# checks board to see if game is over. Return is (bool, winner)
def is_game_over(b):
    # offset by 1 for indexing
    winning_combos = [[0, 1, 2], [3, 4, 5], [6, 7, 8], # horizontal
                      [0, 3, 6], [1, 4, 7], [2, 5, 8], # vertical
                      [0, 4, 8], [2, 4, 6]]            # diagonal

    # check if game is over because of a winning combo
    for combo in winning_combos:
        c1, c2, c3 = combo
        if (b[c1] == b[c2]) and (b[c2] == b[c3]) and (b[c1] != ' '):
            return (True, b[c1].lower())

    # check if game is over because board is full
    for k, v in b.items():
        if v == ' ':
            # game can continue
            return (False, ' ')

    # game is over bc no more spots to play
    return (True, ' ')


# game played between two existing players
def simulate_game(players, strategies):
    # choose player to be x
    print("\nPick X-player")
    for i in range(1, 10+1):
        print(f"{i}: {players[i].record}")
    # get x-player strategy
    x = input("\nENTER -> ").strip()
    while x not in [str(i) for i in range(1, 10+1)]:
        print("Invalid input: Must be player from 1 - 10")
        x = input("\nENTER -> ").strip()
    x_strat = strategies[int(x)]

    # choose player to be o
    print("\nPick O-player")
    rem_players = [j for j in range(1, 10+1) if j != int(x)]
    for i in rem_players:
        print(f"{i}: {players[i].record}")
    # get o-player strategy
    o = input("\nENTER -> ").strip()
    while o not in [str(i) for i in rem_players]:
        print("Invalid input: Must be player from 1 - 10")
        o = input("\nENTER -> ").strip()
    o_strat = strategies[int(o)]

    board = empty_board = { 0: ' ', 1: ' ', 2: ' ',
                            3: ' ', 4: ' ', 5: ' ',
                            6: ' ', 7: ' ', 8: ' ' }
    valid_moves = ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                   'n', 'q']
    turn  = 'x'

    # start game
    while not is_game_over(board)[0]:

        if turn == 'x':
            # get move
            str_board = board_to_str(board)
            move = get_computer_move(x_strat, str_board, valid_moves[:-2])
            # make move and rmeove from valid options
            board[int(move)] = 'X'
            valid_moves.remove(move)
            # switch turn and display board
            turn = 'o'
            print(f"Player {x} made move at {move}" )
            print_board(board)

        # o move
        else:
            # get move
            str_board = board_to_str(board)
            move = get_computer_move(o_strat, str_board, valid_moves[:-2])
            # make move and rmeove from valid options
            board[int(move)] = 'O'
            valid_moves.remove(move)
            # switch turn and display board
            turn = 'x'
            print(f"Player {o} made move at {move}" )
            print_board(board)

    # when game is done, print outcome, and finish
    winner = is_game_over(board)[1]
    if winner == 'x':
        print(f"Winner is {x}")
    elif winner == 'o':
        print(f"Winner is {o}")
    else:
        print("Tie")
    return


# game played between user and an existing player
def one_player_game(name, players, potential_opponents):
    # pick opponent to play against
    print("\nPick Opponent")
    for i in range(1, 10+1):
        print(f"{i}: {players[i].record}")

    opponent = input("\nENTER -> ").strip()
    while opponent not in [str(i) for i in range(1, 10+1)]:
        print("Invalid input: Must be opponent from 1 - 10")
        opponent = input("\nENTER -> ").strip()

    opp_strategy = potential_opponents[int(opponent)]

    # does user want to go first?
    x_OR_o = input("\nWould you like to be X or O? ").lower().strip()
    while x_OR_o not in ['x', 'o']:
        print("\nInvalid input: Must be X or O")
        x_OR_o = input("ENTER -> ").lower().strip()

    print(f"\nGood luck, {name}!")
    board = empty_board = { 0: ' ', 1: ' ', 2: ' ',
                    3: ' ', 4: ' ', 5: ' ',
                    6: ' ', 7: ' ', 8: ' ' }
    valid_moves = ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                   'n', 'q']
    turn  = 'x'

    # if player is 'o', change turn to computer
    if x_OR_o != 'x':
        turn = 'computer'

    else:
        turn = 'player'
        print_board(board)

    while not is_game_over(board)[0]:
        # x move
        if turn == 'player':
            # get move from input
            move = input(f"{name}, enter your move: ").strip()
            # make sure move is valid
            while move not in valid_moves:
                print("\nInvalid input: valid moves are the following, ")
                print(valid_moves[:-2])
                print("[[n]ew game, [q]uit]")
                move = input(f"\n{name}, enter your move: ").strip()

            # if move is a position on board
            if move in valid_moves[:-2]:
                board[int(move)] = 'X' if x_OR_o == 'x' else 'O'
                valid_moves.remove(move)

            # other choices
            else:
                # new game
                if move == 'n':
                    confirm = input('Are you sure you want to play new game? ').strip()
                    while confirm not in ['y', 'n']:
                        print('\nResponse must be [y]es or [n]o')
                        confirm = input('\nAre you sure you want to play new game? ').strip()
                    if confirm == 'y':
                        one_player_game(name, players, potential_opponents)
                        return
                    elif confirm == 'n':
                        continue

                # quit game
                else:
                    confirm = input('Are you sure you want to quit game? ').strip()
                    while confirm not in ['y', 'n']:
                        print('\nResponse must be [y]es or [n]o')
                        confirm = input('\nAre you sure you want to quit game? ').strip()
                    if confirm == 'y':
                        return
                    elif confirm == 'n':
                        continue
            turn = 'computer'
            print('\n\n')
            print_board(board)

        else:
            str_board = board_to_str(board)
            move = get_computer_move(opp_strategy, str_board, valid_moves[:-3])
            board[int(move)] = 'X' if x_OR_o != 'x' else 'O'
            valid_moves.remove(move)
            turn = 'player'
            print(f"Computer made move at {move}" )
            print('\n\n')
            print_board(board)

    # end game
    winner = is_game_over(board)[1]
    if winner == 'x':
        if x_OR_o == 'x':
            print(f"Winner is {name}")
        else:
            print(f"Winner is {opponent}")
    elif winner == 'o':
        if x_OR_o == 'o':
            print(f"Winner is {name}")
        else:
            print(f"Winner is {opponent}")
    else:
        print("Tie")
    return


# game played between two users
def two_player_game(x_name, o_name):
    board = empty_board = { 0: ' ', 1: ' ', 2: ' ',
                    3: ' ', 4: ' ', 5: ' ',
                    6: ' ', 7: ' ', 8: ' ' }
    valid_moves = ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                   'n', 'q']
    turn  = 'x'
    print_board(board)

    # start game
    while not is_game_over(board)[0]:
        # x move
        if turn == 'x':
            # get move from input
            move = input(f"{x_name}, enter your move: ").strip()
            # make sure move is valid
            while move not in valid_moves:
                print("\nInvalid input: valid moves are the following, ")
                print(valid_moves[:-2])
                print("[[n]ew game, [q]uit]")
                move = input(f"\n{x_name}, enter your move: ").strip()

            # if move is a position on board
            if move in valid_moves[:-2]:
                board[int(move)] = 'X'
                valid_moves.remove(move)

            else:
                # new game
                if move == 'n':
                    confirm = input('Are you sure you want to play new game? ').strip()
                    while confirm not in ['y', 'n']:
                        print('\nResponse must be [y]es or [n]o')
                        confirm = input('\nAre you sure you want to play new game? ').strip()
                    if confirm == 'y':
                        two_player_game(x_name, o_name)
                        return
                    elif confirm == 'n':
                        continue

                # quit game
                else:
                    confirm = input('Are you sure you want to quit game? ').strip()
                    while confirm not in ['y', 'n']:
                        print('\nResponse must be [y]es or [n]o')
                        confirm = input('\nAre you sure you want to quit game? ').strip()
                    if confirm == 'y':
                        return
                    elif confirm == 'n':
                        continue
            turn = 'o'
            print('\n\n')
            print_board(board)

        # o move
        else:
            # get move from input
            move = input(f"{o_name}, enter your move: ").strip()
            # make sure move is valid
            while move not in valid_moves:
                print("\nInvalid input: valid moves are the following, ")
                print(valid_moves[:-2])
                print("[[n]ew game, [q]uit]")
                move = input(f"\n{o_name}, enter your move: ").strip()

            # if move is a position on board
            if move in valid_moves[:-2]:
                board[int(move)] = 'O'
                valid_moves.remove(move)

            else:
                # new game
                if move == 'n':
                    confirm = input('Are you sure you want to play new game? ').strip()
                    while confirm not in ['y', 'n']:
                        print('\nResponse must be [y]es or [n]o')
                        confirm = input('\nAre you sure you want to play new game? ').strip()
                    if confirm == 'y':
                        two_player_game(x_name, o_name)
                        return
                    elif confirm == 'n':
                        continue

                # quit game
                else:
                    confirm = input('Are you sure you want to quit game? ').strip()
                    while confirm not in ['y', 'n']:
                        print('\nResponse must be [y]es or [n]o')
                        confirm = input('\nAre you sure you want to quit game? ').strip()
                    if confirm == 'y':
                        return
                    elif confirm == 'n':
                        continue
            turn = 'x'
            print('\n\n')
            print_board(board)

    # end game
    winner = is_game_over(board)[1]
    if winner == 'x':
        print(f"Winner is {x_name}")
    elif winner == 'o':
        print(f"Winner is {o_name}")
    else:
        print("Tie")
    return


class Player:
    '''
    The Player class for the tic tac toe data. Every player will have a class
    representation. The data included for each player is their id, the number of
    games they've played, their record and win % in those games, as well as the
    moves they've made as the x-player and o-player.
    '''

    def __init__(self, player_id):
        self.player_id    = player_id
        self.games_played = 0
        self.record       = {"win": 0, "loss": 0, "tie": 0}
        self.win_pct      = 0.0
        self.moves_as_x   = {}
        self.moves_as_o   = {}
        self.rr_remaining_games = {1: {'x':5, 'o':5}, 2: {'x':5, 'o':5},
                                   3: {'x':5, 'o':5}, 4: {'x':5, 'o':5},
                                   5: {'x':5, 'o':5}, 6: {'x':5, 'o':5},
                                   7: {'x':5, 'o':5}, 8: {'x':5, 'o':5},
                                   9: {'x':5, 'o':5}, 10: {'x':5, 'o':5}}
        # can't play yourself!
        del self.rr_remaining_games[player_id]

    # calculate win % from payers record
    def calc_win_pct(self):
        win  = self.record["win"]  + (self.record["tie"] / 2)
        loss = self.record["loss"] + (self.record["tie"] / 2)
        self.win_pct = win / (win + loss)

    # update data fields once the game is over
    def game_over(self, game_id, game_moves, opponent_id, xo):
        self.games_played += 1
        self.rr_remaining_games[opponent_id][xo] -= 1
        if xo == 'x':
            self.moves_as_x[game_id] = game_moves
        else:
            self.moves_as_o[game_id] = game_moves
        self.calc_win_pct()

    # print out attributes of player (used for debugging)
    def player_print(self):
        print(f"id: {self.player_id}")
        print(f"games_played: {self.games_played}")
        print(f"record: {self.record}")
        print(f"win pct: {self.win_pct}")
        print(f"x_moves: {self.moves_as_x}")
        print(f"o_moves: {self.moves_as_o}")
        print(f"rr_rem: {self.rr_remaining_games}")

    # write attributes of player to txt file (used for final output)
    def player_write(self, file):
        file.write(f"id: {self.player_id}\n")
        file.write(f"games_played: {self.games_played}\n")
        file.write(f"record: {self.record}\n")
        file.write(f"win pct: {self.win_pct}\n")
        file.write(f"x_moves: {self.moves_as_x}\n")
        file.write(f"o_moves: {self.moves_as_o}\n")
        file.write(f"rr_rem: {self.rr_remaining_games}\n")


class Game:
    '''
    The Game class for the tic tac toe data. The fields in the Game class
    include the game_id, what Player is x and which is o, what moves those
    players made, and who won the game.
    '''
    def __init__(self, game_id, player_x, player_o):
        self.game_id  = game_id
        self.player_x = player_x
        self.player_o = player_o
        self.moves_x  = []
        self.moves_o  = []
        self.winner   = None

    # update move fields
    def update_moves(self, move_id, move):
        # x move
        if move_id % 2 == 1:
            self.moves_x.append(move)
        # o move
        else:
            self.moves_o.append(move)

    # determine what player won game
    def find_winner(self):
        # offset by 1 for indexing
        winning_combos = [[0, 1, 2], [3, 4, 5], [6, 7, 8], # horizontal
                          [0, 3, 6], [1, 4, 7], [2, 5, 8], # vertical
                          [0, 4, 8], [2, 4, 6]]            # diagonal

        for combo in winning_combos:
            if set(combo).issubset(set(self.moves_x)):
                self.winner = 'x'
            elif set(combo).issubset(set(self.moves_o)):
                self.winner = 'o'

    # if game is over update fields of the Players in the Game
    def game_over(self):
        self.find_winner()

        if self.winner == 'x':
            self.player_x.record["win"]  += 1
            self.player_o.record["loss"] += 1
        elif self.winner == 'o':
            self.player_o.record["win"]  += 1
            self.player_x.record["loss"] += 1
        else:
            self.player_o.record["tie"]  += 1
            self.player_x.record["tie"]  += 1

        self.player_x.game_over(self.game_id, self.moves_x,
                                self.player_o.player_id, 'x')
        self.player_o.game_over(self.game_id, self.moves_o,
                                self.player_x.player_id, 'o')

    # print out attributes of game (used for debugging)
    def game_print(self):
        print(f"id: {self.game_id}")
        print(f"x_moves: {self.moves_x}")
        print(f"o_moves: {self.moves_o}")
        print(f"winner:{self.winner}")

    # write attributes of game to txt file (used for final output)
    def game_write(self, file):
        file.write(f"id: {self.game_id}\n")
        file.write(f"x_moves: {self.moves_x}\n")
        file.write(f"o_moves: {self.moves_o}\n")
        file.write(f"winner:{self.winner}\n")


# train a decision tree to predict the players moves from moves made
# on specific board placements to learn playing tendencies
def train_for_strats(data, players):

    dt = DecisionTreeClassifier()


    X = {1: [], 2: [], 3: [], 4: [], 5: [],
         6: [], 7: [], 8: [], 9: [], 10: []}
    Y = {1: [], 2: [], 3: [], 4: [], 5: [],
         6: [], 7: [], 8: [], 9: [], 10: []}

    for i in range(1, 220+1):
        temp_data = data.loc[data['game_id'] == i]

        x_player = temp_data['player_x_id'].iloc[0]
        o_player = temp_data['player_o_id'].iloc[0]

        #x_OR_o = 'x' if (temp_data['player_x_id'].iloc[0] == 3) else 'o'

        Y[x_player] += players[x_player].moves_as_x[i]
        Y[o_player] += players[o_player].moves_as_o[i]

        for row in temp_data.iterrows():
            r = row[1]
            if (r['move_id'] % 2 == 1):
                X[x_player].append([r['pre_state']])

            else:
                X[o_player].append([r['pre_state']])

    for i in range(1,10+1):
        X[i] = [label_encoder.transform(list(x[0])) for x in X[i]]

    strategy = {1: None, 2: None, 3: None, 4: None, 5: None,
                6: None, 7: None, 8: None, 9: None, 10: None}

    for i in range(1, 10+1):
        strategy[i] = dt.fit(X[i], Y[i])

    return strategy


# creates Games and Players andparses through data and to see what the results
# of the tictactoe games were in the dataset. Returns the Player classes for
# each player.
def get_results(data):
    # Find results of games played in the dataset
    game_glob   = {}
    player_glob = {1: Player(1), 2: Player(2), 3: Player(3), 4: Player(4),
                   5: Player(5), 6: Player(6), 7: Player(7), 8: Player(8),
                   9: Player(9), 10: Player(10)}

    for i in range(1, 220+1):
        # initialize game info
        temp_data = data.loc[data['game_id'] == i]
        player_x  = player_glob[temp_data['player_x_id'].iloc[0]]
        player_o  = player_glob[temp_data['player_o_id'].iloc[0]]
        game = Game(i, player_x, player_o)

        # play moves
        for row in temp_data.iterrows():
            r = row[1]
            game.update_moves(r['move_id'], r['move'])

        # end game
        game.game_over()
        game_glob[i] = game
        player_glob[player_x.player_id] = player_x
        player_glob[player_o.player_id] = player_o

    f = open('results.txt', 'w')
    for i in sorted(player_glob.keys()):
        player_glob[i].player_write(f)

        # Display results in the results.txt file
        f.write('\n\n')
    f.close()

    return player_glob


# Given the number of players as input, executes the appropriate type of game
def play_tic_tac_toe(num_of_players, player_glob, data):
    if num_of_players == '0':
        strats = train_for_strats(data, player_glob)

        still_playing = True
        while still_playing:
            simulate_game(player_glob, strats)

            still_playing = input("\nWould you like to simulate again? ").strip()
            while still_playing not in ['y', 'n']:
                print('Response must be [y]es or [n]o')
                still_playing = input("ENTER -> ").strip()

            if still_playing == 'n':
                still_playing = False


    elif num_of_players == '1':

        name   = input("\nEnter your name -> ").strip().title()
        strats = train_for_strats(data, player_glob)

        still_playing = True
        while still_playing:
            one_player_game(name, player_glob, strats)

            still_playing = input("\nWould you like to play again? ").strip()
            while still_playing not in ['y', 'n']:
                print('Response must be [y]es or [n]o')
                still_playing = input("ENTER -> ").strip()

            if still_playing == 'n':
                still_playing = False

    else:  # 2 players
        x = input("\nEnter X-player name -> ").strip().title()
        o = input("\nEnter O-player name -> ").strip().title()
        print("\nHave fun!")

        still_playing = True
        while still_playing:
            two_player_game(x, o)

            still_playing = input("\nWould you like to play again? ").strip()
            while still_playing not in ['y', 'n']:
                print('Response must be [y]es or [n]o')
                still_playing = input("ENTER -> ").strip()

            if still_playing == 'n':
                still_playing = False


# Main function. Play Tic-Tac-Toe
def main():
    ttt_data = pd.read_csv("tictactoe-data.csv")
    player_glob = get_results(ttt_data)


    # TIME TO PLAY GAME!!
    # How many players playing?
    print("\nHow many players")
    print("\t0: Simulate Games\n\t1: 1-Player\n\t2: 2-Player\n")
    num_players = input("ENTER -> ").strip()
    while num_players not in ['0', '1' ,'2']:
        print("\nInvalid input: Must be simulated (0) or 1 or 2 players\n")
        num_players = input("ENTER -> ").strip()

    play_tic_tac_toe(num_players, player_glob, ttt_data)

    print("Bye! Thanks for playing!\n")


if __name__ == '__main__':
    # run main
    main()
