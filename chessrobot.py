import chess
import chess.engine

STOCKFISH_PATH = r"C:\Users\alexm\Downloads\progaming\stockfish - Copy\stockfish-windows-x86-64-universal.exe"

engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

board = chess.Board()


def infer_move(board, sense_occupancy):
    matches = []
    for move in board.legal_moves:
        board.push(move)
        if board.occupied == sense_occupancy:
            matches.append(move)
        board.pop()
    return matches

def resolve_move(board, sense_occupancy, last_placed):
    matches = infer_move(board, sense_occupancy)
    if len(matches) == 1:
        return matches[0]
    if len(matches) == 0:
        return None

    candidates = []
    for move in matches:
        if move.to_square == last_placed:
            candidates.append(move)
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) == 0:
        return None
    for move in candidates:
        if move.promotion == chess.QUEEN:
            return move

def parse_sensor_message(line):
    parts = line.split(',')
    if len(parts) != 3 or parts[0] != 'M':
        return None
    try:
        sense_occupancy = int(parts[1], 16)
        last_placed = int(parts[2])
    except ValueError:
        return None
    if not 0 <= last_placed <= 63:
        return None
    return (sense_occupancy, last_placed)

try:
    while True:
        color = input("Enter your color (w/b): ")
        if color.lower() == 'w':
            color = chess.WHITE
            break
        elif color.lower() == 'b':
            color = chess.BLACK
            break
        else:
            print("Invalid color, please enter 'w' or 'b'.")
        
    print(board)
    while not board.is_game_over():
        if board.turn == color:
            player_move = input("Enter your move (e.g., e2e4): ")
            try:    
                board.push_uci(player_move)
            except ValueError:
                print("Invalid move, please try again.")
                continue
            print(board)
        else:
            result = engine.play(board, chess.engine.Limit(time = 1))
            board.push_uci(str(result.move))
            print('Stockfish move:', result.move)
            print(board)

        print(board.result())
except KeyboardInterrupt:
    pass
finally:
    after = board.copy()
    move = chess.Move.from_uci('e2e4')
    after.push(move)
    line = f"M,{after.occupied:016X},{move.to_square}"
    parse_sensor_message(line)
    engine.quit()

