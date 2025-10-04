# Tic Tac Toe - Web Frontend

A modern, beautiful web-based frontend for the Tic Tac Toe game with a Flask backend API.

## Features

- 🎨 Modern, responsive UI with TailwindCSS
- ⚡ Real-time game state management
- 🎮 Smooth animations and transitions
- 🔄 Easy game reset functionality
- 📱 Mobile-friendly design

## Architecture

### Backend (Flask API)
- **File**: `app.py`
- **Port**: 5000
- **Endpoints**:
  - `POST /api/game/new` - Create a new game
  - `GET /api/game/<game_id>` - Get game state
  - `POST /api/game/<game_id>/move` - Make a move
  - `POST /api/game/<game_id>/reset` - Reset game
  - `GET /api/health` - Health check

### Frontend (React + TailwindCSS)
- **File**: `frontend/index.html`
- **Framework**: React 18 (via CDN)
- **Styling**: TailwindCSS (via CDN)
- **Features**: Single-page application with state management

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server

```bash
python app.py
```

The Flask server will start on `http://localhost:5000`

### 3. Open the Frontend

Simply open the `frontend/index.html` file in your web browser:

**Option A: Direct file opening**
- Navigate to the `frontend` folder
- Double-click `index.html` or right-click and "Open with Browser"

**Option B: Using a local server (recommended)**
```bash
cd frontend
python -m http.server 8000
```
Then visit `http://localhost:8000` in your browser

## How to Play

1. The game starts automatically when you open the frontend
2. Player X (Blue) goes first
3. Click on any empty cell to make your move
4. The game alternates between Player X and Player O (Red)
5. Win by getting three in a row (horizontal, vertical, or diagonal)
6. Click "New Game" to start over at any time

## Game Rules

- **Player X**: Blue color, goes first
- **Player O**: Red color, goes second
- **Win Condition**: Three marks in a row (horizontal, vertical, or diagonal)
- **Draw**: All cells filled with no winner

## Troubleshooting

### Backend not connecting
- Make sure the Flask server is running on port 5000
- Check if any firewall is blocking the connection
- Verify the API_BASE_URL in `index.html` matches your backend URL

### CORS errors
- The backend includes CORS support via `flask-cors`
- If issues persist, check browser console for specific errors

### Port already in use
If port 5000 is already in use, you can change it in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to any available port
```
Then update the `API_BASE_URL` in `frontend/index.html` accordingly.

## Technology Stack

- **Backend**: Python 3, Flask, Flask-CORS
- **Frontend**: React 18, TailwindCSS
- **Game Logic**: Reuses existing `tic_tac_toe.py` module

## Future Enhancements

- [ ] Add AI opponent mode
- [ ] Game history and statistics
- [ ] Multiplayer over network
- [ ] Sound effects
- [ ] Dark mode toggle
- [ ] Save/load game state
- [ ] Leaderboard

## License

Same as the main project.
