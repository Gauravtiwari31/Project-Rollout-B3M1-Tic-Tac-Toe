#!/usr/bin/env python3
"""
Tic Tac Toe - Two player console game with optional save/resume.

File persistence format (stored in game_state.txt next to this script):
Row 1: comma-separated values for top row (e.g., X,O,X)
Row 2: comma-separated values for middle row (e.g., -,O,-)
Row 3: comma-separated values for bottom row (e.g., X,-,-)
Row 4: Player Turn: N  (where N is 1 for Player 1 (X) or 2 for Player 2 (O))

Empty cells are represented with '-'.
"""

from __future__ import annotations

import os
import sys
from typing import List, Optional, Tuple


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GAME_STATE_FILE = os.path.join(SCRIPT_DIR, "game_state.txt")


def get_player_symbol(player_number: int) -> str:
    return "X" if player_number == 1 else "O"


def get_player_number(symbol: str) -> int:
    return 1 if symbol.upper() == "X" else 2


def initialize_board() -> List[str]:
    return ["-"] * 9


def render_board(board: List[str]) -> None:
    """Print the board to console. Empty cells show their 1-9 position numbers."""
    def cell_value(index: int) -> str:
        return board[index] if board[index] != "-" else str(index + 1)

    print("Current Board:")
    print(f" {cell_value(0)} | {cell_value(1)} | {cell_value(2)}")
    print("---+---+---")
    print(f" {cell_value(3)} | {cell_value(4)} | {cell_value(5)}")
    print("---+---+---")
    print(f" {cell_value(6)} | {cell_value(7)} | {cell_value(8)}")


WINNING_COMBINATIONS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


def check_winner(board: List[str]) -> Optional[str]:
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] != "-" and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_draw(board: List[str]) -> bool:
    return all(cell != "-" for cell in board) and check_winner(board) is None


def save_game(board: List[str], current_player_symbol: str) -> None:
    rows = [
        ",".join(board[0:3]),
        ",".join(board[3:6]),
        ",".join(board[6:9]),
    ]
    player_line = f"Player Turn: {get_player_number(current_player_symbol)}"
    with open(GAME_STATE_FILE, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(row + "\n")
        f.write(player_line + "\n")
    print("Game state saved!\n(Current board and player turn recorded in game_state.txt)")


def load_game() -> Optional[Tuple[List[str], str]]:
    if not os.path.exists(GAME_STATE_FILE):
        return None
    try:
        with open(GAME_STATE_FILE, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        if len(lines) < 4:
            return None
        row1 = [x.strip() for x in lines[0].split(",")]
        row2 = [x.strip() for x in lines[1].split(",")]
        row3 = [x.strip() for x in lines[2].split(",")]
        if not (len(row1) == len(row2) == len(row3) == 3):
            return None
        flat = row1 + row2 + row3
        if any(x not in {"X", "O", "-"} for x in flat):
            return None
        if not lines[3].lower().startswith("player turn:"):
            return None
        try:
            player_num = int(lines[3].split(":", 1)[1].strip())
        except ValueError:
            return None
        if player_num not in (1, 2):
            return None
        current_player_symbol = get_player_symbol(player_num)
        return flat, current_player_symbol
    except Exception:
        return None


def delete_saved_game() -> None:
    try:
        if os.path.exists(GAME_STATE_FILE):
            os.remove(GAME_STATE_FILE)
    except OSError:
        pass


def prompt_resume_if_available() -> Optional[Tuple[List[str], str]]:
    loaded = load_game()
    if not loaded:
        return None
    while True:
        choice = input("A saved game was found. Resume it? (y/n): ").strip().lower()
        if choice in {"y", "yes"}:
            return loaded
        if choice in {"n", "no"}:
            return None
        print("Please enter 'y' or 'n'.")


def main() -> None:
    print("Welcome to Tic Tac Toe!")
    print("1) Two Players")
    print("2) Play vs AI")
    mode = input("Choose mode (1-2): ").strip()
    if mode == "2":
        # Defer to AI runner in submodule
        try:
            import importlib
            import sys as _sys
            if SCRIPT_DIR not in _sys.path:
                _sys.path.insert(0, SCRIPT_DIR)
            module = importlib.import_module("tictactoe_ai.play_ai")
            module.main()
            return
        except Exception as e:
            print(f"Failed to start AI mode: {e}")
            print("Falling back to Two Players mode.\n")

    print("Player 1: X")
    print("Player 2: O\n")

    resumed = prompt_resume_if_available()
    if resumed:
        board, current_player = resumed
    else:
        board = initialize_board()
        current_player = "X"

    while True:
        render_board(board)
        player_num = get_player_number(current_player)
        move = input(
            f"\nPlayer {player_num}, enter your move (1-9) or 's' to save and exit: "
        ).strip().lower()

        if move in {"s", "save"}:
            save_game(board, current_player)
            # Exit after saving to match a simple console flow
            return

        if not move.isdigit():
            print("Please enter a number between 1 and 9, or 's' to save.")
            continue
        cell_index = int(move) - 1
        if cell_index < 0 or cell_index >= 9:
            print("Invalid position. Choose a number between 1 and 9.")
            continue
        if board[cell_index] != "-":
            print("That cell is already taken. Choose another one.")
            continue

        board[cell_index] = current_player

        winner = check_winner(board)
        if winner:
            render_board(board)
            print(f"\nPlayer {get_player_number(winner)} ({winner}) wins! Congratulations!")
            # Game finished; clean up any saved state
            delete_saved_game()
            return

        if is_draw(board):
            render_board(board)
            print("\nIt's a draw!")
            delete_saved_game()
            return

        # Switch player
        current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting. Goodbye!")
        sys.exit(0)


