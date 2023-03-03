import os
from db import db
from sqlalchemy.sql import text


def add_mood(mood, user_id):
    sql = "INSERT INTO moods (mood, user_id) VALUES (:mood, :user_id)"
    sql2 = text(sql)
    db.session.execute(sql2, {"mood": mood, "user_id": user_id})
    db.session.commit()

def show_moods(user_id):
    sql = "SELECT mood, sent_at FROM moods WHERE user_id=user_id"
    sql2 = text(sql)
    moods = db.session.execute(sql2)
    moodlist = moods.fetchall()
    for row in moodlist:
        print(row)

