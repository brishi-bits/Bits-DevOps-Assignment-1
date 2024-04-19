from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from configparser import ConfigParser
import os

app = Flask(__name__)

# Construct the path to the config file
current_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_dir, 'config.ini')

parser = ConfigParser()
parser.read(config_file_path)

MONGODB_URL = parser.get('MongoDB', 'MONGODB_URL')

print(f"MONGODB_URL_Rishi: '{MONGODB_URL}'")
client = MongoClient(MONGODB_URL)

db = client.get_database("DATABASE1")
recipes_collection = db['recipes']

@app.route('/recipes', methods=['GET'])
def get_all_recipes():
    recipes = list(recipes_collection.find({}))
    if len(recipes) == 0:
        return jsonify({"message": "No recipes exist in the database"})
    else:
        # Convert ObjectId to string
        for recipe in recipes:
            recipe['_id'] = str(recipe['_id'])
        return jsonify(recipes)

@app.route('/recipes/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = recipes_collection.find_one({"_id": ObjectId(recipe_id)})
    if recipe:
        # Convert ObjectId to string
        recipe['_id'] = str(recipe['_id'])
        return jsonify(recipe)
    else:
        return jsonify({"message": f"Recipe with id {recipe_id} does not exist"}), 404

@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.json
    result = recipes_collection.insert_one(data)
    new_recipe_id = str(result.inserted_id)
    return jsonify({"message": "Recipe created successfully", "recipe_id": new_recipe_id}), 201

@app.route('/recipes/<recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    data = request.json
    result = recipes_collection.update_one({"_id": ObjectId(recipe_id)}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"message": f"Recipe with id {recipe_id} does not exist"}), 404
    else:
        return jsonify({"message": f"Recipe with id {recipe_id} updated successfully"})

@app.route('/recipes/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    result = recipes_collection.delete_one({"_id": ObjectId(recipe_id)})
    if result.deleted_count == 0:
        return jsonify({"message": f"Recipe with id {recipe_id} does not exist"}), 404
    else:
        return jsonify({"message": f"Recipe with id {recipe_id} deleted successfully"}), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
