# Mini exercise : petite API de recherche sur une collection MongoDB (thème : manga)
# Flask = mini serveur web Python ; chaque @app.get / @app.post = une route (URL).
# Lancer : python api_manga.py  puis ouvrir http://127.0.0.1:5000/search?keyword=one
import re                                        # re.escape : neutralise les caractères spéciaux du mot cherché
from bson import ObjectId                        # ObjectId = type de l'_id MongoDB
from bson.errors import InvalidId
from flask import Flask, jsonify, request
from connexion import get_client

app = Flask(__name__)
mangas = get_client()["manga_db"]["mangas"]      # entité principale : Manga

def to_json(doc):
    doc["_id"] = str(doc["_id"])                 # ObjectId n'est pas du JSON : on le convertit en texte
    return doc

def seed():
    """Remplit la collection avec quelques mangas si elle est vide."""
    if mangas.count_documents({}) == 0:
        mangas.insert_many([
            {"name": "One Piece", "description": "Pirates searching for the One Piece treasure", "genre": "action", "volumes": 108},
            {"name": "Death Note", "description": "A notebook that kills anyone whose name is written in it", "genre": "thriller", "volumes": 12},
            {"name": "Naruto", "description": "A young ninja who wants to become Hokage", "genre": "action", "volumes": 72},
            {"name": "Yotsuba&!", "description": "Daily life of a cheerful little girl", "genre": "comedy", "volumes": 15},
        ])

@app.post("/items")                              # Create : POST /items avec un JSON dans le corps
def create_item():
    data = request.get_json(silent=True) or {}
    if not data.get("name"):
        return jsonify(error="field 'name' is required"), 400
    res = mangas.insert_one(data)
    return jsonify(_id=str(res.inserted_id)), 201

@app.get("/items/<item_id>")                     # Read : GET /items/:id
def read_item(item_id):
    try:
        doc = mangas.find_one({"_id": ObjectId(item_id)})
    except InvalidId:
        return jsonify(error="invalid id"), 400
    return (jsonify(to_json(doc)), 200) if doc else (jsonify(error="not found"), 404)

@app.get("/items")                               # liste paginée : GET /items?page=1&limit=10
def list_items():
    page, limit = int(request.args.get("page", 1)), int(request.args.get("limit", 10))
    docs = mangas.find().skip((page - 1) * limit).limit(limit)   # skip/limit = pagination
    return jsonify([to_json(d) for d in docs])

@app.get("/search")                              # GET /search?keyword=...&genre=...&max_volumes=...
def search():
    kw = request.args.get("keyword", "")
    rx = {"$regex": re.escape(kw), "$options": "i"}               # $regex + option i = insensible à la casse
    query = {"$or": [{"name": rx}, {"description": rx}]}           # recherche dans 2 champs
    if request.args.get("genre"):                                  # filtre supplémentaire 1 : genre exact
        query["genre"] = request.args["genre"]
    if request.args.get("max_volumes"):                            # filtre supplémentaire 2 : volumes <= n
        query["volumes"] = {"$lte": int(request.args["max_volumes"])}
    return jsonify([to_json(d) for d in mangas.find(query)])

if __name__ == "__main__":
    seed()
    app.run(debug=True)
