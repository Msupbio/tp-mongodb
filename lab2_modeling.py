# Lab 2 « NoSQL Modeling » : users, posts, comments, likes
# Choix de modèle : les commentaires et les likes sont IMBRIQUÉS dans chaque post
# (on les lit toujours avec le post) ; les users restent une collection à part (référence par _id).
from pprint import pprint
from connexion import get_client

db = get_client()["social"]
db.users.drop(); db.posts.drop()

# 1) at least 3 users
ids = db.users.insert_many([
    {"username": "alice", "email": "alice@example.com"},
    {"username": "bob",   "email": "bob@example.com"},
    {"username": "chloe", "email": "chloe@example.com"},
]).inserted_ids
alice, bob, chloe = ids

# 2) at least 5 posts (author = référence vers users._id)
db.posts.insert_many([
    {"author_id": alice, "title": "Hello MongoDB", "content": "My first post", "comments": [], "likes": []},
    {"author_id": alice, "title": "NoSQL vs SQL",  "content": "Documents vs tables", "comments": [], "likes": []},
    {"author_id": bob,   "title": "Python tips",   "content": "Use pymongo", "comments": [], "likes": []},
    {"author_id": chloe, "title": "Atlas cluster", "content": "Free tier M0", "comments": [], "likes": []},
    {"author_id": bob,   "title": "Indexes",       "content": "Speed up queries", "comments": [], "likes": []},
])

# 3) comments on some posts — $push ajoute un élément au tableau
db.posts.update_one({"title": "Hello MongoDB"}, {"$push": {"comments": {"user_id": bob, "text": "Welcome!"}}})
db.posts.update_one({"title": "Hello MongoDB"}, {"$push": {"comments": {"user_id": chloe, "text": "Nice post"}}})
db.posts.update_one({"title": "Python tips"},   {"$push": {"comments": {"user_id": alice, "text": "Thanks!"}}})

# 4) likes — $addToSet ajoute seulement si absent (un user ne like qu'une fois)
for title, users in {"Hello MongoDB": [bob, chloe], "Python tips": [alice, chloe, bob], "Indexes": [alice]}.items():
    for u in users:
        db.posts.update_one({"title": title}, {"$addToSet": {"likes": u}})

print("\n1) All posts")
for p in db.posts.find({}, {"title": 1, "_id": 0}):           # projection : seulement le titre
    print(" -", p["title"])

print("\n2) Posts of user 'alice'")
for p in db.posts.find({"author_id": alice}, {"title": 1, "_id": 0}):
    print(" -", p["title"])

print("\n3) Comments on 'Hello MongoDB'")
pprint(db.posts.find_one({"title": "Hello MongoDB"}, {"comments": 1, "_id": 0})["comments"])

print("\n4) Post with the most likes")   # $size = longueur du tableau ; tri décroissant ; 1er résultat
top = list(db.posts.aggregate([
    {"$project": {"title": 1, "nb_likes": {"$size": "$likes"}}},
    {"$sort": {"nb_likes": -1}},
    {"$limit": 1},
]))
pprint(top)

print("\n5) Number of posts per user")   # $group = GROUP BY ; $lookup = jointure vers users
pprint(list(db.posts.aggregate([
    {"$group": {"_id": "$author_id", "nb_posts": {"$sum": 1}}},
    {"$lookup": {"from": "users", "localField": "_id", "foreignField": "_id", "as": "user"}},
    {"$project": {"_id": 0, "username": {"$arrayElemAt": ["$user.username", 0]}, "nb_posts": 1}},
    {"$sort": {"nb_posts": -1}},
])))
