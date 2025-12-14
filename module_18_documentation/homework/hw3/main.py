from flask import Flask, request
from jsonrpcserver import method, dispatch

app = Flask(__name__)

@method
def add(a: int, b: int) -> int:
    return a + b

@method
def sub(a: int, b: int) -> int:
    return a - b

@method
def mul(a: int, b: int) -> int:
    return a * b

@method
def div(a: int, b: int) -> float:
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    return a / b

@app.route("/api", methods=["POST"])
def api():
    response = dispatch(request.get_data().decode())
    return response

if __name__ == "__main__":
    app.run(debug=True)