def add_review(name, low, neutral, high):
    sql = text("INSERT INTO effects (name, low, neutral, high) VALUES (:name, :low, :neutral, :high)")
    db.session.execute(sql)
    db.session.commit()

def show_reviews(name):
    sql1 = text("SELECT count(*) FROM effects WHERE name=:name AND low = true") 

