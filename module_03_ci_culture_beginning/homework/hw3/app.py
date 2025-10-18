from flask import Flask, request, jsonify

app = Flask(__name__)

storage = {}

@app.route("/add/", methods=["POST"])
def add():
    data = request.get_json()
    date = data.get("date")
    amount = data.get("amount")

    if not (isinstance(date, str) and len(date) == 8 and date.isdigit()):
        raise TypeError("Date must be in format YYYYMMDD")

    if not isinstance(amount, (int, float)):
        raise TypeError("Amount must be a number")

    storage[date] = amount
    return jsonify({"status": "ok", "date": date, "amount": amount})

@app.route("/calculate/sum", methods=["GET"])
def calculate_sum():
    total = sum(storage.values()) if storage else 0
    return jsonify({"result": total})

@app.route("/calculate/average", methods=["GET"])
def calculate_average():
    if not storage:
        return jsonify({"result": 0})
    avg = sum(storage.values()) / len(storage)
    return jsonify({"result": avg})

if __name__ == "__main__":
    app.run(debug=True)