from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Определяем пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'rooms.json')


def load_rooms():
    """Безопасная загрузка данных из JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


@app.route('/')
def index():
    # Ошибка была здесь: вместо "index.templates" нужно указать "index.html"
    # Flask автоматически ищет этот файл внутри папки /templates/
    return render_template('index.html')


@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    try:
        rooms = load_rooms()
        return jsonify(rooms)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/book', methods=['POST'])
def book():
    data = request.json
    room_id = data.get('room_id')
    nights = int(data.get('nights', 1))

    rooms = load_rooms()
    room = next((r for r in rooms if r['id'] == room_id), None)

    if not room:
        return jsonify({'status': 'error', 'message': 'Room not found'}), 404

    total_price = room['price'] * nights
    return jsonify({
        'status': 'success',
        'total_price': total_price,
        'room_name': room['name']
    })


if __name__ == '__main__':
    # Создаем папку data, если она отсутствует
    if not os.path.exists(os.path.join(BASE_DIR, 'data')):
        os.makedirs(os.path.join(BASE_DIR, 'data'))

    print("Сервер запущен! Перейдите по адресу: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)