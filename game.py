import chess
import chess.engine
from FakeSensorBoard import FakeSensorBoard
from chessrobot import parse_sensor_message, resolve_move

STOCKFISH_PATH = r"C:\Users\alexm\Downloads\progaming\stockfish - Copy\stockfish-windows-x86-64-universal.exe"

def play(sensorboard):
    fake = sensorboard
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

    try:
        while not board.is_game_over():
            line = fake.readline()
            parsed = parse_sensor_message(line)

            if parsed is None:
                print("could not parse line")
                continue
            else:
                occupancy, last_placed = parsed
                final = resolve_move(board, occupancy, last_placed)
                if final is None:
                    print("could not resolve move")
                    continue
                board.push(final)
                print(final)
            if board.is_game_over():
                break
            else:
                result = engine.play(board, chess.engine.Limit(time = 0.5))
                fake.robot_move(str(result.move))
                print('Stockfish move:', result.move)
    except KeyboardInterrupt:
        pass
    finally:
        engine.quit()

if __name__ == "__main__":
    play(FakeSensorBoard())

        
        
