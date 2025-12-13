from flask import Flask, request, jsonify
import operator

app = Flask(__name__)

@app.route("/api", methods=["POST"])
def rpc():
    data = request.get_json()
    method = data.get("method")
    params = data.get("params", {})
    a, b = params.get("a"), params.get("b")

    try:
        if method == "calc.add":
            result = operator.add(a, b)
        elif method == "calc.sub":
            result = operator.sub(a, b)
        elif method == "calc.mul":
            result = operator.mul(a, b)
        elif method == "calc.div":
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            result = operator.truediv(a, b)
        else:
            return jsonify({"error": "Unknown method"}), 400

        return jsonify({"jsonrpc": "2.0", "result": result, "id": data.get("id")})
    except Exception as e:
        return jsonify({"jsonrpc": "2.0", "error": str(e), "id": data.get("id")}), 400

if __name__ == "__main__":
    app.run(debug=True)