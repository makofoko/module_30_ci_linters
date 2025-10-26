class ThresholdValidator:
    """Класс‑валидатор: можно использовать как объект"""
    def __init__(self, min_value: int = 1):
        self.min_value = min_value

    def __call__(self, value: str) -> int:
        try:
            num = int(value)
            if num < self.min_value:
                raise ValueError(f"Value must be >= {self.min_value}")
            return num
        except Exception:
            raise ValueError("Invalid threshold value")

from flask import request

@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    try:
        threshold_param = request.args.get("threshold", "1")

        threshold = validate_threshold(threshold_param) 
        validator = ThresholdValidator(1)
        threshold = validator(threshold_param)
        result = subprocess.check_output(["uptime"], text=True).strip()
        return f"Current uptime is {result}, threshold={threshold}"
    except ValueError as ve:
        return f"Validation error: {ve}", 400
    except Exception as e:
        return f"Error retrieving uptime: {e}", 500
