import os
from pymongo import MongoClient

db = MongoClient(os.environ["MONGODB_URI"])["social"]

# Users
alice, bob, chloe = db.users.insert_many([
    {"username": "alice"},
    {"username": "bob"},
    {"username": "chloe"},
]).inserted_ids

# Posts (comments and likes embedded in each post)
db.posts.insert_many([
    {"author_id": alice, "title": "Hello MongoDB", "comments": [], "likes": []},
    {"author_id": alice, "title": "NoSQL vs SQL", "comments": [], "likes": []},
    {"author_id": bob, "title": "Python tips", "comments": [], "likes": []},
    {"author_id": chloe, "title": "Atlas cluster", "comments": [], "likes": []},
    {"author_id": bob, "title": "Indexes", "comments": [], "likes": []},
])

# Comments
db.posts.update_one({"title": "Hello MongoDB"}, {"$push": {"comments": {"user_id": bob, "text": "Welcome!"}}})
db.posts.update_one({"title": "Hello MongoDB"}, {"$push": {"comments": {"user_id": chloe, "text": "Nice post"}}})
db.posts.update_one({"title": "Python tips"}, {"$push": {"comments": {"user_id": alice, "text": "Thanks!"}}})

# Likes
db.posts.update_one({"title": "Hello MongoDB"}, {"$addToSet": {"likes": {"$each": [bob, chloe]}}})
db.posts.update_one({"title": "Python tips"}, {"$addToSet": {"likes": {"$each": [alice, bob, chloe]}}})
db.posts.update_one({"title": "Indexes"}, {"$addToSet": {"likes": alice}})

# 1. All posts
print(list(db.posts.find()))

# 2. A user's posts
print(list(db.posts.find({"author_id": alice})))

# 3. Comments on a post
print(db.posts.find_one({"title": "Hello MongoDB"}, {"comments": 1, "_id": 0}))

# 4. Post with the most likes
print(list(db.posts.aggregate([
    {"$project": {"title": 1, "nb_likes": {"$size": "$likes"}}},
    {"$sort": {"nb_likes": -1}},
    {"$limit": 1},
])))

# 5. Number of posts per user
print(list(db.posts.aggregate([
    {"$group": {"_id": "$author_id", "nb_posts": {"$sum": 1}}},
])))
