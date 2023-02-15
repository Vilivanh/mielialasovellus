from db import db

def choose(category, free, lowcost, highcost):
    frees = "SELECT (*) FROM private_actions WHERE free = TRUE"
    frees2  ="SELECT (*) FROM actions WHERE free = TRUE"
    frees3 = "SELECT (*) FROM private_actions WHERE category=:category AND free = TRUE"
    frees4 = "SELECT (*) FROM actions WHERE category=:category AND free = TRUE"

def random(category, free, lowcost, highcost):

