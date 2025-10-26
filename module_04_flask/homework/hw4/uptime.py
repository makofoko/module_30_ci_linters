import subprocess
from flask import Flask

app = Flask(__name__)

@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    try:
        result = subprocess.check_output(["uptime"], text=True).strip()
        return f"Current uptime is {result}"
    except Exception as e:
        return f"Error retrieving uptime: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)