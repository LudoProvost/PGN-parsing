import chess.pgn
import time
import random
from io import StringIO

# returns the number of consecutive checks made before checkmate
def get_num_consecutive_checks(game):

    #[consecutive checks given by white, consecutive checks given by black]
    consecutive_checks = [0,0]

    board = game.board()
    for number, move in enumerate(game.mainline_moves(), start=1):
        check_count = 0
        player = 0 if (board.turn == chess.WHITE) else 1
        # print(f"Move {number} ({board.turn}): {board.san(move)}")

        # see if move gives check
        if (board.gives_check(move)):
            consecutive_checks[player] = consecutive_checks[player] + 1
        else:
            consecutive_checks[player] = 0

        board.push(move)

        if (board.is_checkmate()):
            if (consecutive_checks[player] == None):
                return 0
            return consecutive_checks[player]

# Function to read and process games from a PGN file
def process_games_from_file(pgn_file_path):
    check_counts = []
    highest_check_count_games = []
    game_num = 0
    with open(pgn_file_path, 'r', encoding='utf-8') as pgn:
        while True:
            game_num += 1
            game = chess.pgn.read_game(pgn)
            highest_check_count = 0
            highest_check_count_games = []
            
            if game is None:
                break  # End of file reached
            
            if (game.headers["Result"] == "0-1" or "1-0"):
                #
                check_count = get_num_consecutive_checks(game)
                
                # edge case, decisive winner but no checkmates
                if (check_count is None):
                    check_count = 0
                # if this is the highest recorded check count yet, change size of check_counts
                while (len(check_counts)-1 < check_count):
                    check_counts.append(0)

                # print(len(check_counts))
                check_counts[check_count] = check_counts[check_count] + 1

                # if (check_count == highest_check_count):

                #     # highest_check_count_games.append(game)
                #     highest_check_count_games[0] = game
                # elif (check_count > highest_check_count):
                #     # highest_check_count_games.clear
                #     # highest_check_count_games.append(game)
                #     highest_check_count = check_count
                #     highest_check_count_games[0] = game


                if (check_count >= 27):
                    # highest_check_count_games.append([check_count, game])
                    dir = "highest_check_games/game" + str(game_num) + "_checkcount" + str(check_count) + ".pgn"
                    print_game_to_pgn(game, dir)


    # print_highest_games(highest_check_count_games)
    return check_counts

def print_game_to_pgn(game, dir):
    print(game, file=open(dir, "w"), end="\n\n")

def print_highest_games(games):
    dir = "highest_check_games/game"
    for i in range(0, len(games)):
        game = games[i]
        game_dir = dir + str(i) + "_checkcount" + str(game[0]) + ".pgn"
        print_game_to_pgn(game[1], game_dir)


# START
start_time = time.time()
pgn_file_path = 'decompressed_db/lichess_db_standard_rated_2014-09.pgn'
check_counts = process_games_from_file(pgn_file_path)
print(check_counts)
end_time = time.time()
print(f"processing time (minutes): {(end_time-start_time)/60}")