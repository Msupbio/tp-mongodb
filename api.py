import os
import re
from bson import ObjectId
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
mangas = MongoClient(os.environ["MONGODB_URI"])["manga_db"]["mangas"]


def to_json(doc):
    doc["_id"] = str(doc["_id"])
    return doc


@app.post("/items")
def create_item():
    result = mangas.insert_one(request.get_json())
    return jsonify(_id=str(result.inserted_id)), 201


@app.get("/items/<item_id>")
def read_item(item_id):
    doc = mangas.find_one({"_id": ObjectId(item_id)})
    return (jsonify(to_json(doc)), 200) if doc else (jsonify(error="not found"), 404)


@app.get("/items")
def list_items():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    return jsonify([to_json(d) for d in mangas.find().skip((page - 1) * limit).limit(limit)])


@app.get("/search")
def search():
    regex = {"$regex": re.escape(request.args.get("keyword", "")), "$options": "i"}
    query = {"$or": [{"name": regex}, {"description": regex}]}
    if "genre" in request.args:
        query["genre"] = request.args["genre"]
    return jsonify([to_json(d) for d in mangas.find(query)])


if __name__ == "__main__":
    app.run()
