import subprocess
import os
from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

class CodeForm(FlaskForm):
    code = StringField(validators=[DataRequired()])
    timeout = IntegerField(validators=[DataRequired(), NumberRange(min=1, max=30)])


def run_python_code_in_subprocess(code: str, timeout: int):
    """
    Запускает Python-код в отдельном процессе с ограничением по времени.
    Возвращает stdout/stderr или сообщение о превышении тайм-аута.
    """
    try:
        cmd = ["prlimit", "--nproc=1:1", "python3", "-c", code]

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        try:
            stdout, stderr = proc.communicate(timeout=timeout)
            return {"stdout": stdout, "stderr": stderr, "timeout": False}
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            return {
                "stdout": stdout,
                "stderr": stderr,
                "timeout": True,
                "message": f"Исполнение кода превысило {timeout} секунд"
            }

    except Exception as e:
        return {"error": str(e)}


@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()
    if form.validate_on_submit():
        code = form.code.data
        timeout = form.timeout.data
        result = run_python_code_in_subprocess(code, timeout)
        return jsonify(result)
    else:
        return jsonify({"errors": form.errors}), 400


if __name__ == '__main__':
    app.run(debug=True)
