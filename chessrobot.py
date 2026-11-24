import chess
import chess.engine

STOCKFISH_PATH = r"C:\Users\alexm\Downloads\progaming\stockfish - Copy\stockfish-windows-x86-64-universal.exe"

engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

board = chess.Board()

#infers what move was played based on what the sensors see. 
def infer_move(board, sense_occupancy):# sensed occupancy is a 64 bit integer representing the current board state. bit 0 = a1, bit 64 = h8
    matches = []
    # pushs every legal move and checks if the resulting board state matches the sensed occupancy
    # if board state matches, add the move to the list of matches. Then pop the move to restore the board state.
    for move in board.legal_moves:
        board.push(move)
        if board.occupied == sense_occupancy:
            matches.append(move)
        board.pop()
    return matches

#resolves the list from infer_move to a single move. 
def resolve_move(board, sense_occupancy, last_placed):
    matches = infer_move(board, sense_occupancy)
    #returns the move if there is only one item in match.
    if len(matches) == 1:
        return matches[0]
    #returns none if there is nothing in matches. Maybe an illegal move or an error in sensor data. 
    if len(matches) == 0:
        return None

    #if there are multiple items in matches. 
    candidates = []
    for move in matches:
        #if a piece can capture two different pieces, it looks the same in matches. 
        #to resolve this, sensor data can show us where the most recent piece was placed.
        #append all the new moves into a new list called candidates.
        if move.to_square == last_placed:
            candidates.append(move)
    #if there is one match in candiates, return that move.
    if len(candidates) == 1:
        return candidates[0]
    #if there are no matches in candidates, return none.
    if len(candidates) == 0:
        return None
    #promotions can include knight, bishiop, rook, and queen.
    #they all look like the same move to the sensors.
    #we just assume the player promoted to queen and return promtion to queen as the move. 
    for move in candidates:
        if move.promotion == chess.QUEEN:
            return move

#creates sensed occupancy and lastplaced from sensor data.
def parse_sensor_message(line):
    #The message format should be "M,<sensed occupancy>,<last placed square>"
    parts = line.split(',')
    #checks to see if message starts with M and has 3 parts.
    #returns none if not true. 
    if len(parts) != 3 or parts[0] != 'M':
        return None
    #tries to convert sensed occupancy and last placed into integers. 
    #if it fails, return none.
    try:
        sense_occupancy = int(parts[1], 16)
        last_placed = int(parts[2])
    except ValueError:
        return None
    #checks to see if last placed is between 0 and 64
    #returns none if not
    if not 0 <= last_placed <= 63:
        return None
    return (sense_occupancy, last_placed)

#stock fish game loop
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

