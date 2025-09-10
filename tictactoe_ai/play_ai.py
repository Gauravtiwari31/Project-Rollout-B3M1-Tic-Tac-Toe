#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from typing import Dict, List

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_MISC_DIR = os.path.dirname(SCRIPT_DIR)

# Reuse board rendering from the base game by importing directly
if PROJECT_MISC_DIR not in sys.path:
    sys.path.insert(0, PROJECT_MISC_DIR)
try:
    from tic_tac_toe import (
        render_board,
        initialize_board,
        get_player_number,
        check_winner,
        is_draw,
    )
except Exception:
    # Fallback minimal render if import path differs
    def initialize_board() -> List[str]:
        return ["-"] * 9

    def render_board(board: List[str]) -> None:
        def cell_value(index: int) -> str:
            return board[index] if board[index] != "-" else str(index + 1)
        print("Current Board:")
        print(f" {cell_value(0)} | {cell_value(1)} | {cell_value(2)}")
        print("---+---+---")
        print(f" {cell_value(3)} | {cell_value(4)} | {cell_value(5)}")
        print("---+---+---")
        print(f" {cell_value(6)} | {cell_value(7)} | {cell_value(8)}")

    def get_player_number(symbol: str) -> int:
        return 1 if symbol.upper() == "X" else 2

    WINNING_COMBINATIONS = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]

    def check_winner(board: List[str]):
        for a, b, c in WINNING_COMBINATIONS:
            if board[a] != "-" and board[a] == board[b] == board[c]:
                return board[a]
        return None

    def is_draw(board: List[str]) -> bool:
        return all(cell != "-" for cell in board) and check_winner(board) is None

try:
    from .engine import board_to_key, get_best_move
except Exception:
    # Allow running as a standalone script
    if SCRIPT_DIR not in sys.path:
        sys.path.insert(0, SCRIPT_DIR)
    from engine import board_to_key, get_best_move  # type: ignore


POLICY_FILE = os.path.join(SCRIPT_DIR, "ai_policy.json")


def load_policy() -> Dict[str, int]:
    if not os.path.exists(POLICY_FILE):
        return {}
    try:
        with open(POLICY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def prompt_human_move(board: List[str], current_player: str) -> int:
    while True:
        move = input(
            f"\nPlayer {get_player_number(current_player)} ({current_player}), enter your move (1-9): "
        ).strip()
        if not move.isdigit():
            print("Please enter a number between 1 and 9.")
            continue
        cell = int(move) - 1
        if cell < 0 or cell >= 9:
            print("Invalid position. Choose a number between 1 and 9.")
            continue
        if board[cell] != "-":
            print("That cell is already taken. Choose another one.")
            continue
        return cell


def choose_ai_move(board: List[str], current_player: str, policy: Dict[str, int]) -> int:
    key = board_to_key(board, current_player)
    if key in policy:
        return policy[key]
    return get_best_move(board, current_player)


def main() -> None:
    print("Starting Human vs AI mode (X = Human, O = AI by default).")
    board = initialize_board()
    human_symbol = "X"
    ai_symbol = "O"
    policy = load_policy()

    current = "X"
    while True:
        render_board(board)
        if current == human_symbol:
            move = prompt_human_move(board, current)
        else:
            move = choose_ai_move(board, current, policy)
            print(f"\nAI chooses position {move + 1}.")
        board[move] = current

        winner = check_winner(board)
        if winner:
            render_board(board)
            if winner == human_symbol:
                print("\nYou win! 🎉")
            else:
                print("\nAI wins! 🤖")
            return
        if is_draw(board):
            render_board(board)
            print("\nIt's a draw!")
            return

        current = ai_symbol if current == human_symbol else human_symbol


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting. Goodbye!")


