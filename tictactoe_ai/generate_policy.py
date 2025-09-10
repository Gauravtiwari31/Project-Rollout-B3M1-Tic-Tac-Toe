#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from typing import Dict, List

try:
    from .engine import (
        check_winner,
        is_draw,
        available_moves,
        switch_player,
        get_best_move,
        board_to_key,
    )
except Exception:
    # Allow running as a standalone script
    import sys as _sys
    _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from engine import (  # type: ignore
        check_winner,
        is_draw,
        available_moves,
        switch_player,
        get_best_move,
        board_to_key,
    )


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
POLICY_FILE = os.path.join(SCRIPT_DIR, "ai_policy.json")


def enumerate_states(board: List[str], player: str, seen: Dict[str, bool]) -> None:
    key = "".join(board) + f"|{player}"
    if key in seen:
        return
    seen[key] = True

    if check_winner(board) or is_draw(board):
        return

    for move in available_moves(board):
        board[move] = player
        enumerate_states(board, switch_player(player), seen)
        board[move] = "-"


def build_policy() -> Dict[str, int]:
    # Enumerate all legal states starting from empty board and X to move
    initial_board = ["-"] * 9
    seen: Dict[str, bool] = {}
    enumerate_states(initial_board, "X", seen)

    policy: Dict[str, int] = {}
    for key in list(seen.keys()):
        board_str, player = key.split("|")
        board = list(board_str)
        # Skip finished states
        if check_winner(board) or is_draw(board):
            continue
        best = get_best_move(board, player)
        policy[key] = best
    return policy


def main() -> None:
    policy = build_policy()
    with open(POLICY_FILE, "w", encoding="utf-8") as f:
        json.dump(policy, f, separators=(",", ":"))
    print(f"Generated policy with {len(policy)} states at {POLICY_FILE}")


if __name__ == "__main__":
    main()


