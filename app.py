import threading
from flask import Flask, render_template, jsonify, request
from game.controller import GameController
from utils.config import GameConfig
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, start_http_server

app = Flask(__name__)

# Initialize game with default config
config = GameConfig()
game = GameController(config)

# Start Prometheus metrics server in a separate thread (port 8000)
def start_prometheus():
    start_http_server(8000)  # This allows Prometheus to scrape metrics separately     // access prometheus through specified Prometheus metrics server localhost:8000/metrics 

threading.Thread(target=start_prometheus, daemon=True).start()

@app.route('/')
def index():
    game.start_game()
    return render_template('index.html')

# Expose Prometheus metrics via Flask as well
@app.route('/metrics')                  # access prometheus through Flask localhost:5000/metrics or 
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST} 

@app.route('/move', methods=['POST'])
def make_move():
    direction = request.json.get('direction')
    if direction:
        valid_move = game.handle_move(direction)
        return jsonify({
            'grid': game.board.grid,
            'score': game.board.score,
            'gameOver': game.board.is_game_over(),
            'validMove': valid_move
        })
    return jsonify({'error': 'Invalid direction'}), 400

@app.route('/new_game', methods=['POST'])
def new_game():
    global game # reference the global game object
    game = GameController(config)  # Reset the entire game object
    # print(game.board.grid)
    game.start_game()
    return jsonify({
        'grid': game.board.grid,
        'score': game.board.score,
        'gameOver': False
    })

if __name__ == '__main__':
    app.run(debug=False)
    # app.run(host='127.0.0.1', port=5000, debug=True)  # Allows both `localhost` and `127.0.0.1`