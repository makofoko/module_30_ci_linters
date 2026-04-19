import json

class MyWSGIApp:
    routes = {}

    @classmethod
    def route(cls, path):
        def decorator(func):
            cls.routes[path] = func
            return func
        return decorator

    def __call__(self, environ, start_response):
        path = environ.get("REQUEST_URI", "/")
        if path in self.routes:
            response = self.routes[path]()
            status = "200 OK"
        elif path.startswith("/hello/"):
            name = path.split("/")[-1]
            response = json.dumps({"response": f"Hello, {name}!"}, indent=4)
            status = "200 OK"
        else:
            response = json.dumps({"error": "Not Found"}, indent=4)
            status = "404 Not Found"

        headers = [("Content-Type", "application/json")]
        start_response(status, headers)
        return [response.encode("utf-8")]


app = MyWSGIApp()

@app.route("/hello")
def say_hello():
    return json.dumps({"response": "Hello, world!"}, indent=4)