from sqlalchemy.sql import text
from db import db

def add_review(name, low, neutral, high):
    sql = "INSERT INTO effects (name, low, neutral, high) VALUES (:name, :low, :neutral, :high)"
    sql2 = text(sql)
    db.session.execute(sql2, {"name":name, "low":low, "neutral":neutral, "high":high})
    db.session.commit()

def show_reviews(userid):
    user_id = userid
    sql = "SELECT name FROM actions UNION SELECT name FROM private_actions WHERE creator_id=:user_id GROUP BY name"
    sql2 = text(sql)
    
    results = db.session.execute(sql2, {"user_id":user_id}).fetchall()
    reslist = []
    res2 = []
    for i in results:
        res2.append(i[0])
    for result in res2:
        action_name = result
        sql = "SELECT COUNT(*) FROM effects WHERE action_name=:action_name AND low=TRUE"
        sql2 = text(sql)
        lw2 = db.session.execute(sql2, {"action_name":action_name})
        lw = lw2.first()[0]
        db.session.commit()
        sql3 = "SELECT COUNT(*) FROM effects WHERE action_name=:action_name AND neutral=TRUE"
        sql4 = text(sql3)
        neut2 = db.session.execute(sql4, {"action_name":action_name})
        neut = neut2.first()[0] 
        db.session.commit()
        sql5 = "SELECT COUNT(*) FROM effects WHERE action_name=:action_name AND high=TRUE"
        sql6 = text(sql5)
        hg2 = db.session.execute(sql6, {"action_name":action_name})
        hg = hg2.first()[0]
        db.session.commit()
        reslist.append((action_name, lw, neut, hg))
    return reslist

def t_filter_reviews(categories, prices, criteria):
    results = []
    a = ""
    b = ""
    c = ""
    for price in prices:
        if price == "Ilmainen":
            a = " AND free=TRUE"
        if price == "Edullinen":
            b = " AND lowcost=TRUE"
        if price == "Kallis":
            c = " AND highcost=TRUE"
    
    for category in categories:
        sql_test ="SELECT name, (SELECT COUNT(*) FROM effects WHERE category=category"  
        if len(a)>0:
            sql_test +=a
        if len(b)>0:
            sql_test +=b
        if len(c)>0:
            sql_test +=c
        sql_test +=") FROM actions"
         
        sql2 = text(sql_test)
        temp_results = db.session.execute(sql2, {"category":category}).fetchall()
        results.append([result for result in temp_results])
    print(results)
    return results

def filter_reviews(categories, prices, criteria, userid):
    user_id=userid
    sql = "SELECT name FROM actions UNION SELECT name FROM private_actions WHERE creator_id=:user_id"
    sql2 = text(sql)
    results = db.session.execute(sql2, {"user_id":user_id}).fetchall()
    print(results)
    
    if len(categories)>0 or len(prices)>0:
        results=[]
        if len(prices) == 0:
            for category in categories:
                sql = "SELECT name FROM actions WHERE category=:category UNION SELECT name FROM private_actions WHERE category=:category AND creator_id=:user_id"
                sql2 = text(sql)
                temp_results = db.session.execute(sql2, {"category":category, "user_id":user_id}).fetchall()
                results.append([result[0] for result in temp_results])
        elif len(categories) == 0:
            if "Ilmainen" in prices:
                sql = "SELECT name FROM actions WHERE free=TRUE UNION SELECT name FROM private_actions WHERE free=TRUE AND creator_id=:user_id"
                sql2 = text(sql)
                temp_results = db.session.execute(sql2, {"user_id":user_id}).fetchall()
                results.append([result[0] for result in temp_results])
            if "Edullinen" in prices:
                sql = "SELECT name FROM actions WHERE lowcost=TRUE UNION SELECT name FROM private_actions WHERE lowcost=TRUE AND creator_id=:user_id"
                sql2 = text(sql)
                temp_results = db.session.execute(sql2, {"user_id":user_id}).fetchall()
                results.append([result[0] for result in temp_results])
            if "Kallis" in prices:
                sql = "SELECT name FROM actions WHERE highcost=TRUE UNION SELECT name FROM private_actions WHERE highcost=TRUE AND creator_id=:user_id"
                sql2 = text(sql)
                temp_results = db.session.execute(sql2, {"user_id":user_id}).fetchall()
                results.append([result[0] for result in temp_results])
        else:
             for category in categories:
                for price in prices:
                    if price == "Ilmainen":
                        sql = "SELECT name FROM actions WHERE category=:category AND free=TRUE UNION SELECT name FROM private_actions WHERE category=:category AND free=TRUE AND creator_id=:user_id"
                        sql2 = text(sql)
                        temp_results = db.session.execute(sql2, {"category":category, "user_id":user_id}).fetchall()
                        results.append([result[0] for result in temp_results])
                    if price == "Edullinen":
                        sql = "SELECT name FROM actions WHERE category=:category AND lowcost=TRUE UNION SELECT name FROM private_actions WHERE category=:category AND lowcost=TRUE AND creator_id=:user_id"
                        sql2 = text(sql)
                        temp_results = db.session.execute(sql2, {"category":category, "user_id":user_id}).fetchall()
                        results.append([result[0] for result in temp_results])
                    if price == "Kallis":
                        sql = "SELECT name FROM actions WHERE category=:category AND highcost=TRUE UNION SELECT name FROM private_actions WHERE category=:category AND highcost=TRUE AND creator_id=:user_id"
                        sql2 = text(sql)
                        temp_results = db.session.execute(sql2, {"category":category, "user_id":user_id}).fetchall()
                        results.append([result[0] for result in temp_results])                        
    reslist = []
    res2 = []
    print(results)
    for resultlist in results:
        for result in resultlist:
            res2.append(result)
    print(res2)
    for result in res2:
        action_name = result
        sql = "SELECT COUNT(*) FROM effects WHERE action_name=:action_name AND low=TRUE"
        sql2 = text(sql)
        lw2 = db.session.execute(sql2, {"action_name":action_name})
        lw = lw2.first()[0]
        db.session.commit()
        sql3 = "SELECT COUNT(*) FROM effects WHERE action_name=:action_name AND neutral=TRUE"
        sql4 = text(sql3)
        neut2 = db.session.execute(sql4, {"action_name":action_name})
        neut = neut2.first()[0]
        db.session.commit()
        sql5 = "SELECT COUNT(*) FROM effects WHERE action_name=:action_name AND high=TRUE"
        sql6 = text(sql5)
        hg2 = db.session.execute(sql6, {"action_name":action_name})
        hg = hg2.first()[0]
        db.session.commit()
        if criteria == "2":
            if lw == 0:
                reslist.append((action_name, lw, neut, hg))
        elif criteria == "3":
            if hg > lw:
                reslist.append((action_name, lw, neut, hg))
        elif criteria == "4":
            sumall = lw+neut+hg
            half = sumall/2
            if hg > half:
                reslist.append((action_name, lw, neut, hg))
        else:
            reslist.append((action_name, lw, neut, hg))
    return reslist
