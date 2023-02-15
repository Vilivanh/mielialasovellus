from db import db
from sqlalchemy.sql import text

def add_action(name, category, creator_id, free, lowcost, highcost):
    sql = """INSERT INTO private_actions (name, category, creator_id, free, lowcost, highcost)
             VALUES (:name, :category, :creator_id, :free, :lowcost, :highcost) RETURNING id"""
    action_id = db.session.execute(text(sql), {"name":name, "category":category, "creator_id":creator_id, "free":free, "lowcost":lowcost, "highcost":highcost}).fetchone()[0]
    db.session.commit()
    return action_id
