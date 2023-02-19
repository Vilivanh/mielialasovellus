from db import db
from random import randint

def showall():
    sql1 = "SELECT * FROM actions"
    sql2 = "SELECT * FROM private_actions"
    listing = db.session.execute(sql1).fetchall()
    list2 = db.session.execute(sql2).fetchall()
    listing.append(list2)
    return listing


def decide(category, free, lowcost, highcost):
    if free == True:
        if lowcost == False:
            if highcost == False:
                sql1 = "SELECT name, category FROM actions WHERE category=:category AND free = t AND lowcost = f AND highcost = f"
            else:
                sql1 = "SELECT name, category FROM actions WHERE category=:category AND free = t AND lowcost = f AND highcost = t"
        else:
            if highcost == False:
                sql1 = "SELECT name, category FROM actions WHERE category=:category AND free = t AND lowcost = t AND highcost = f"
            else:
                sql1 = "SELECT name, category FROM actions WHERE category=:category AND free = t AND lowcost = t AND highcost = t"
    else:
        if lowcost == False:
            if highcost == True:
                sql1 = "SELECT name, category FROM actions WHERE category=:category AND free = f AND lowcost = f AND highcost = t"
        else:
            if highcost == True:
                sql1 = "SELECT name, category FROM actions WHERE category=:category AND free = f AND lowcost = t AND highcost = t"
            else:
                sql1 = "SELECT name, category FROM actions WHERE category=:category AND free = f AND lowcost = f AND highcost = t"

    return db.session.execute(sql1).fetchall()

def random(category, free, lowcost, highcost):
    listing = decide(category, free, lowcost, highcost)
    listlen = len(listing)
    random_number = randint(0, listlen)
    return listing[random_number]

