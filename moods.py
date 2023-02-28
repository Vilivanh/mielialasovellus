import os
from db import db
from sqlalchemy.sql import text


def add_mood(mood, user_id):
    sql = "INSERT INTO moods (mood, user_id) VALUES (:mood, :user_id)"
    sql2 = text(sql)
    db.session.execute(sql2, {"mood": int(mood), "user_id": user_id})
    db.session.commit()
