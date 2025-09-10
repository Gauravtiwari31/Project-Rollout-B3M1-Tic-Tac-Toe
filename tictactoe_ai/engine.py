from __future__ import annotations

from typing import List, Optional, Tuple


WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


def check_winner(board: List[str]) -> Optional[str]:
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] != "-" and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_draw(board: List[str]) -> bool:
    return all(cell != "-" for cell in board) and check_winner(board) is None


def available_moves(board: List[str]) -> List[int]:
    return [i for i, v in enumerate(board) if v == "-"]


def switch_player(symbol: str) -> str:
    return "O" if symbol == "X" else "X"


def minimax(board: List[str], player: str, maximizing_for: str) -> Tuple[int, Optional[int]]:
    winner = check_winner(board)
    if winner == maximizing_for:
        return 1, None
    elif winner == switch_player(maximizing_for):
        return -1, None
    elif is_draw(board):
        return 0, None

    if player == maximizing_for:
        best_score = -2
        best_move: Optional[int] = None
        for move in available_moves(board):
            board[move] = player
            score, _ = minimax(board, switch_player(player), maximizing_for)
            board[move] = "-"
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move
    else:
        best_score = 2
        best_move = None
        for move in available_moves(board):
            board[move] = player
            score, _ = minimax(board, switch_player(player), maximizing_for)
            board[move] = "-"
            if score < best_score:
                best_score = score
                best_move = move
        return best_score, best_move


def get_best_move(board: List[str], player: str) -> int:
    """Return the best move index (0-8) for player using minimax."""
    _, move = minimax(board[:], player, player)
    # Fallback: first available (should not happen)
    return move if move is not None else available_moves(board)[0]


def board_to_key(board: List[str], current_player: str) -> str:
    return "".join(board) + f"|{current_player}"


