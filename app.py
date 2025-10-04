#!/usr/bin/env python3
"""
Flask backend API for Tic Tac Toe game.
Provides REST endpoints for the web frontend.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from typing import List, Optional, Dict, Any
import os

# Import game logic from existing module
from tic_tac_toe import (
    initialize_board,
    check_winner,
    is_draw,
    get_player_symbol,
    get_player_number,
    WINNING_COMBINATIONS
)

# Import AI engine
try:
    from tictactoe_ai.engine import get_best_move
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("Warning: AI module not available")

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# In-memory game state (can be extended to use database)
games: Dict[str, Dict[str, Any]] = {}


def generate_game_id() -> str:
    """Generate a simple game ID."""
    import uuid
    return str(uuid.uuid4())


@app.route('/api/game/new', methods=['POST'])
def new_game():
    """Create a new game."""
    data = request.get_json() or {}
    ai_mode = data.get('ai_mode', False)
    
    game_id = generate_game_id()
    games[game_id] = {
        'board': initialize_board(),
        'current_player': 'X',
        'winner': None,
        'is_draw': False,
        'game_over': False,
        'ai_mode': ai_mode,
        'human_symbol': 'X',
        'ai_symbol': 'O'
    }
    return jsonify({
        'game_id': game_id,
        'board': games[game_id]['board'],
        'current_player': games[game_id]['current_player'],
        'ai_mode': ai_mode
    })


@app.route('/api/game/<game_id>', methods=['GET'])
def get_game(game_id: str):
    """Get current game state."""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    return jsonify({
        'game_id': game_id,
        'board': game['board'],
        'current_player': game['current_player'],
        'winner': game['winner'],
        'is_draw': game['is_draw'],
        'game_over': game['game_over']
    })


@app.route('/api/game/<game_id>/move', methods=['POST'])
def make_move(game_id: str):
    """Make a move in the game."""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    
    if game['game_over']:
        return jsonify({'error': 'Game is already over'}), 400
    
    data = request.get_json()
    position = data.get('position')
    
    if position is None or not isinstance(position, int):
        return jsonify({'error': 'Invalid position'}), 400
    
    if position < 0 or position >= 9:
        return jsonify({'error': 'Position out of range'}), 400
    
    if game['board'][position] != '-':
        return jsonify({'error': 'Cell already taken'}), 400
    
    # Make the move
    game['board'][position] = game['current_player']
    
    # Check for winner
    winner = check_winner(game['board'])
    if winner:
        game['winner'] = winner
        game['game_over'] = True
        return jsonify({
            'board': game['board'],
            'current_player': game['current_player'],
            'winner': winner,
            'is_draw': False,
            'game_over': True
        })
    
    # Check for draw
    if is_draw(game['board']):
        game['is_draw'] = True
        game['game_over'] = True
        return jsonify({
            'board': game['board'],
            'current_player': game['current_player'],
            'winner': None,
            'is_draw': True,
            'game_over': True
        })
    
    # Switch player
    game['current_player'] = 'O' if game['current_player'] == 'X' else 'X'
    
    # If AI mode and it's AI's turn, make AI move
    ai_move_position = None
    if game.get('ai_mode', False) and game['current_player'] == game.get('ai_symbol', 'O'):
        if AI_AVAILABLE:
            ai_move_position = get_best_move(game['board'], game['current_player'])
            game['board'][ai_move_position] = game['current_player']
            
            # Check for winner after AI move
            winner = check_winner(game['board'])
            if winner:
                game['winner'] = winner
                game['game_over'] = True
                return jsonify({
                    'board': game['board'],
                    'current_player': game['current_player'],
                    'winner': winner,
                    'is_draw': False,
                    'game_over': True,
                    'ai_move': ai_move_position
                })
            
            # Check for draw after AI move
            if is_draw(game['board']):
                game['is_draw'] = True
                game['game_over'] = True
                return jsonify({
                    'board': game['board'],
                    'current_player': game['current_player'],
                    'winner': None,
                    'is_draw': True,
                    'game_over': True,
                    'ai_move': ai_move_position
                })
            
            # Switch back to human player
            game['current_player'] = 'O' if game['current_player'] == 'X' else 'X'
    
    return jsonify({
        'board': game['board'],
        'current_player': game['current_player'],
        'winner': None,
        'is_draw': False,
        'game_over': False,
        'ai_move': ai_move_position
    })


@app.route('/api/game/<game_id>/reset', methods=['POST'])
def reset_game(game_id: str):
    """Reset an existing game."""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    old_game = games[game_id]
    games[game_id] = {
        'board': initialize_board(),
        'current_player': 'X',
        'winner': None,
        'is_draw': False,
        'game_over': False,
        'ai_mode': old_game.get('ai_mode', False),
        'human_symbol': old_game.get('human_symbol', 'X'),
        'ai_symbol': old_game.get('ai_symbol', 'O')
    }
    
    return jsonify({
        'game_id': game_id,
        'board': games[game_id]['board'],
        'current_player': games[game_id]['current_player'],
        'ai_mode': games[game_id]['ai_mode']
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
