import os
from flask import Flask, request, jsonify
from celery import group
from celery.result import GroupResult
from homework.celery_app import celery_app
from homework.image import blur_image_task
from homework.mail import send_email_task
from homework.utils import make_zip

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route("/blur", methods=["POST"])
def blur():
    email = request.form.get("email")
    files = request.files.getlist("images")

    task_group = []
    filenames = []

    for f in files:
        filepath = os.path.join(UPLOAD_FOLDER, f.filename)
        f.save(filepath)
        filenames.append(filepath)
        task_group.append(blur_image_task.s(filepath))

    group_result = group(task_group).apply_async()
    group_result.save()

    zip_path = make_zip(filenames, os.path.join(RESULT_FOLDER, "results.zip"))
    send_email_task.delay("order123", email, zip_path)

    return jsonify({"group_id": group_result.id})

@app.route("/status/<task_id>", methods=["GET"])
def status(task_id):
    result = GroupResult.restore(task_id, app=celery_app)
    if not result:
        return jsonify({"error": "No such task"}), 404

    task_info = []
    for r in result.results:
        task_info.append({
            "id": r.id,
            "state": r.state,
            "traceback": r.traceback
        })

    return jsonify({
        "completed": result.completed_count(),
        "total": len(result),
        "ready": result.ready(),
        "successful": result.successful(),
        "tasks": task_info
    })

@app.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get("email")
    with open("subscribers.txt", "a") as f:
        f.write(email + "\n")
    return jsonify({"message": f"{email} subscribed"})

@app.route("/unsubscribe", methods=["POST"])
def unsubscribe():
    email = request.form.get("email")
    if os.path.exists("subscribers.txt"):
        with open("subscribers.txt", "r") as f:
            lines = f.readlines()
        with open("subscribers.txt", "w") as f:
            for line in lines:
                if line.strip() != email:
                    f.write(line)
    return jsonify({"message": f"{email} unsubscribed"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)