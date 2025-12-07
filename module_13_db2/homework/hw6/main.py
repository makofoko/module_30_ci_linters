import sqlite3
import datetime

TRAINING_DAY = {
    0: "football",
    1: "hockey",
    2: "chess",
    3: "sup",
    4: "boxing",
    5: "dota2",
    6: "chessboxing"
}

def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    """
    Обновляет расписание смен с учётом кружков.
    """
    cursor.execute("DELETE FROM table_friendship_schedule;")

    cursor.execute("SELECT id, hobby FROM table_friendship_workers;")
    workers = cursor.fetchall()

    hobby_groups = {}
    for wid, hobby in workers:
        hobby_groups.setdefault(hobby, []).append(wid)

    start_date = datetime.date(2025, 1, 1)
    for day_offset in range(366):
        current_date = start_date + datetime.timedelta(days=day_offset)
        weekday = current_date.weekday()
        forbidden_hobby = TRAINING_DAY[weekday]

        available_workers = [wid for wid, hobby in workers if hobby != forbidden_hobby]

        if len(available_workers) < 10:
            raise ValueError(f"Недостаточно работников для дня {current_date}")

        chosen = available_workers[:10]

        for wid in chosen:
            cursor.execute(
                "INSERT INTO table_friendship_schedule (worker_id, work_date) VALUES (?, ?);",
                (wid, current_date.isoformat())
            )