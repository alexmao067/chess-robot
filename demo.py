import chess
from FakeSensorBoard import FakeSensorBoard
from chessrobot import parse_sensor_message, resolve_move

fake = FakeSensorBoard()
board = chess.Board()

line = fake.readline()
print('line:', line)

parsed = parse_sensor_message(line)
if parsed is None:
    print("couldl not parse line")
else:
    occupancy, last_placed = parsed
    final = resolve_move(board, occupancy, last_placed)
    print('final move:', final)

