from flask import Flask, send_from_directory, jsonify, request
import os
import json
import logging

# Загрузка конфигурации
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "music_dir": os.path.expanduser("~/.vibe/music"),
    "port": 5000,
    "host": "0.0.0.0"
}

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=4)

with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

MUSIC_DIR = config.get("music_dir", DEFAULT_CONFIG["music_dir"])
PORT = config.get("port", DEFAULT_CONFIG["port"])
HOST = config.get("host", DEFAULT_CONFIG["host"])

# Создание папки с музыкой, если её нет
os.makedirs(MUSIC_DIR, exist_ok=True)

# Настройка логирования
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "server.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return send_from_directory("static", "index.html")

@app.route('/music')
def list_music():
    """Возвращает список треков в ~/.vibe/music."""
    tracks = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav', '.ogg'))]
    logging.info(f"Список треков запрошен: {tracks}")
    return jsonify(tracks)

@app.route('/music/<filename>')
def serve_music(filename):
    """Отдаёт аудиофайл."""
    logging.info(f"Трек запущен: {filename}")
    return send_from_directory(MUSIC_DIR, filename)

@app.route('/api/play', methods=['POST'])
def play_track():
    """Логирует факт воспроизведения трека."""
    data = request.json
    track = data.get("track")
    logging.info(f"Пользователь запустил трек: {track}")
    return jsonify({"status": "playing", "track": track})

@app.route('/api/next')
def next_track():
    """Логирует переключение на следующий трек."""
    logging.info("Следующий трек")
    return jsonify({"status": "next"})

@app.route('/api/prev')
def prev_track():
    """Логирует переключение на предыдущий трек."""
    logging.info("Предыдущий трек")
    return jsonify({"status": "prev"})

@app.route('/api/volume', methods=['POST'])
def set_volume():
    """Логирует изменение громкости."""
    data = request.json
    volume = data.get("volume")
    logging.info(f"Громкость установлена: {volume}")
    return jsonify({"status": "volume_changed", "volume": volume})

@app.route('/api/status')
def status():
    """Возвращает текущий статус сервера."""
    return jsonify({"status": "running", "music_dir": MUSIC_DIR})

if __name__ == '__main__':
    logging.info(f"Запуск сервера на {HOST}:{PORT}")
    app.run(host=HOST, port=PORT)
