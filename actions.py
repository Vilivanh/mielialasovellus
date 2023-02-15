from db import db
from sqlalchemy.sql import text


def get_all_actions():
    sql = "SELECT id, name, category FROM actions ORDER BY name"
    sql2 = text(sql)
    return db.session.execute(sql2).fetchall()

def add_action(name, category, free, lowcost, highcost, creator_id):
    sql = """INSERT INTO private_actions (name, category, free, lowcost, highcost, creator_id)
             VALUES (:name, :category, :free, :lowcost, :highcost, :creator_id)"""
    sql2 = text(sql)
    action_id = db.session.execute(sql2, {"name":name, "category": category, "free":free, "lowcost":lowcost, "highcost":highcost, "creator_id":creator_id})
    db.session.commit()
    return action_id

