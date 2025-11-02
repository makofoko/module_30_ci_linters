import json
from flask import Flask, request

app = Flask(__name__)

logs_storage = []


@app.route('/log', methods=['POST'])
def log():
    """
    Принимаем логи от сервисов через POST.
    """
    try:
        data = request.get_json(force=True)
        logs_storage.append(data)
        return {"status": "ok", "message": "log received"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400


@app.route('/logs', methods=['GET'])
def logs():
    """
    Отдаём все накопленные логи в HTML <pre>.
    """
    return "<pre>" + json.dumps(logs_storage, indent=2, ensure_ascii=False) + "</pre>"


if __name__ == "__main__":
    app.run(port=5000, debug=False)
