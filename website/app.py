import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play')
def play():
    return render_template('play.html')

@app.route('/game')
def game():
    """Serve the Pygame web build"""
    return send_from_directory(os.path.join(app.static_folder, 'game'), 'index.html')

@app.route('/game/<path:filename>')
def serve_game_files(filename):
    """Serve game assets (JS, CSS, WASM, etc)"""
    return send_from_directory(os.path.join(app.static_folder, 'game'), filename)

if __name__ == '__main__':
    # Render provides PORT env var
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
