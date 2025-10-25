import shlex
import subprocess
from flask import Flask, request

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps_command():
    args = request.args.getlist("arg")

    safe_args = [shlex.quote(arg) for arg in args]

    command = ["ps"] + safe_args

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout
    except subprocess.CalledProcessError as e:
        return f"<pre>Error executing ps: {e}</pre>", 500

    return f"<pre>{output}</pre>"


if __name__ == "__main__":
    app.run(debug=True)