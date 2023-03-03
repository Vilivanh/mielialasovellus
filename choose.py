from db import db
from random import randint
from sqlalchemy.sql import text

def showall():
    sql1 = "SELECT * FROM actions"
    sql2 = "SELECT * FROM private_actions"
    listing = db.session.execute(sql1).fetchall()
    list2 = db.session.execute(sql2).fetchall()
    listing.append(list2)
    return listing


def decide_self(categories, free, lowcost, highcost):
    listing = []
    for category in categories:
        if category == "1":
            category_name = "Nautinto"
        elif category == "2":
            category_name = "Viihde"
        elif category == "3": 
            category_name = "Liikunta"
        elif category == "4":
            category_name = "Muu"
        sql1 = "SELECT name, category FROM actions WHERE category=:category AND (free = TRUE OR lowcost = TRUE OR highcost = TRUE)"  
        sql2 = text(sql1)
        #sql3 = "SELECT name, category FROM private_actions WHERE category=:category AND (free = t OR lowcost = t OR highcost = t)"
        #sql4 = text(sql3)
        result = db.session.execute(sql2, {"name": name, "category": category_name, "free": free, "lowcost": lowcost, "highcost": highcost}).fetchall()
        for row in result:
            listing.append(row)
        
    return listing

def random_action(categories, free, lowcost, highcost):
    listing = []
    if free == True:
        for category in categories:
            sql1 = "SELECT name, category FROM actions WHERE category=:category AND free = TRUE"
            sql2 = text(sql1)
            results = db.session.execute(sql2, {"category": category}).fetchall()
            for result in results:
                listing.append((result[0], result[1], "Ilmainen"))
    if lowcost == True:
        for category in categories:
            sql1 = "SELECT name, category FROM actions WHERE category=:category AND lowcost = TRUE"
            sql2 = text(sql1)
            results = db.session.execute(sql2, {"category": category}).fetchall()
            for result in results:
                listing.append((result[0], result[1], "Edullinen"))
    if highcost == True:
        for category in categories:
            sql1 = "SELECT name, category FROM actions WHERE category=:category AND highcost = TRUE"
            sql2 = text(sql1)
            results = db.session.execute(sql2, {"category": category}).fetchall()
            for result in results:
                listing.append((result[0], result[1], "Kallis"))
        
    listlen = len(listing)
    if listlen > 1:
        random_number = randint(0, listlen-1)
    else:
        random_number = 0
    return listing[random_number]

