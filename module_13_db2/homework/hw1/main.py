import sqlite3

def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:
    """
    Проверяет, испортилась ли вакцина в грузовике.
    Условия: температура должна быть в диапазоне [-20, -16].
    Если хотя бы три измерения подряд вне диапазона — вакцина испорчена.
    """

    cursor.execute("""
        SELECT COUNT(*)
        FROM table_truck_with_vaccine
        WHERE truck_number = ?
        AND (temperature_in_celsius NOT BETWEEN 16 AND 20)
    """, (truck_number,))
    temps = [row[0] for row in cursor.fetchall()]

    bad_count = 0
    for t in temps:
        if t < -20 or t > -16:
            bad_count += 1
            if bad_count >= 3:
                return True
        else:
            bad_count = 0

    return False
