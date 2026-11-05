# Lab 1 « Discovering MongoDB » : base e-commerce (users, products, orders)
# Équivalent Python (pymongo) des commandes mongosh ; les commandes mongosh sont en commentaire.
from pprint import pprint                     # pprint = affichage lisible des documents
from connexion import get_client

client = get_client()

# 1) Database creation  — mongosh : use ecommerce
db = client["ecommerce"]                      # la base est créée au 1er document inséré
for c in ("users", "products", "orders"):     # repartir de zéro si on relance le script
    db[c].drop()

# 2) + 3) Collections créées automatiquement à l'insertion
# mongosh : db.users.insertMany([...])
db.users.insert_many([
    {"name": "Alice", "age": 25, "city": "Paris"},
    {"name": "Bob",   "age": 32, "city": "Lille"},
    {"name": "Chloé", "age": 28, "city": "Paris"},
])
# mongosh : db.products.insertMany([...])
db.products.insert_many([
    {"name": "Laptop",     "price": 899, "category": "Electronics"},
    {"name": "Mouse",      "price": 25,  "category": "Electronics"},
    {"name": "Desk chair", "price": 120, "category": "Furniture"},
    {"name": "Notebook",   "price": 5,   "category": "Stationery"},
])
# Une commande = le nom du client, les produits achetés (tableau imbriqué) et le total
# mongosh : db.orders.insertOne({...})
db.orders.insert_one({
    "user": "Alice",
    "products": [{"name": "Laptop", "price": 899}, {"name": "Mouse", "price": 25}],
    "total": 924,
})

# 4) Queries
print("\n-- All users  (db.users.find())")
for u in db.users.find():
    pprint(u)
print("\n-- Products with price > 50  (db.products.find({ price: { $gt: 50 } }))")
for p in db.products.find({"price": {"$gt": 50}}):   # $gt = greater than (>)
    pprint(p)
print("\n-- Users living in Paris  (db.users.find({ city: 'Paris' }))")
for u in db.users.find({"city": "Paris"}):
    pprint(u)
print("\n-- All orders  (db.orders.find())")
for o in db.orders.find():
    pprint(o)

# 5) Update — mongosh : db.users.updateOne({ name: 'Bob' }, { $set: { age: 33 } })
r = db.users.update_one({"name": "Bob"}, {"$set": {"age": 33}})   # $set = remplace ce champ seulement
print("\n-- Update:", r.modified_count, "user modified ->", db.users.find_one({"name": "Bob"}))

# 6) Deletion — mongosh : db.products.deleteOne({ name: 'Notebook' })
r = db.products.delete_one({"name": "Notebook"})
print("-- Delete:", r.deleted_count, "product deleted ; remaining:", db.products.count_documents({}))
