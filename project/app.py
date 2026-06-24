from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Главная
@app.route("/")
def home():
    return render_template("index.templates")

# Вход
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form["phone"]
        password = request.form["password"]
        account = session.get("account")
        if account and account["phone"] == phone and account["password"] == password:
            session["user"] = account["childName"]
            return redirect(url_for("profile"))
        else:
            return "Неверный номер или пароль!"
    return render_template("login.templates")

# Регистрация
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        childName = request.form["childName"]
        phone = request.form["phone"]
        password = request.form["password"]
        session["account"] = {"childName": childName, "phone": phone, "password": password}
        return redirect(url_for("login"))
    return render_template("register.templates")

# Профиль
@app.route("/profile")
def profile():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))
    return render_template("profile.templates", user=user)

# Выход
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
