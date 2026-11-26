#fake sensor board for testing chessrobot.py without a physical chessboard.
import chess

class FakeSensorBoard:
    def __init__(self):
        self.board = chess.Board()

    def readline(self):
        text = input("make yo move: (e2e4): ")

        try:
            move = chess.Move.from_uci(text)
        except ValueError:
            return 'value error'
        
        if move not in self.board.legal_moves:
            return 'illegal move'

        self.board.push(move)
        return "M,{:x},{}".format(self.board.occupied, move.to_square)

    def robot_move(self, uci):
        self.board.push(chess.Move.from_uci(uci))