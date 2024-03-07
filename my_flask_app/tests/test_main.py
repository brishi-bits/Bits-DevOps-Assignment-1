# tests/test_main.py
import pytest
import sys
import os
import json

# Ensure the app directory is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_recipes(client):
    response = client.get('/recipes')    
    data = json.loads(response.get_data(as_text=True))
    recipe = data[0]
    assert recipe["_id"] == "65e8d27aa94adff3dd8cdc60"
    assert recipe["cuisine"] == "Indian"
    assert recipe["ingredients"] == "3L milk, curd"
    assert recipe["instructions"] == "1.Boil milk and add little curd later."
    assert recipe["name"] == "curd"
    assert recipe["servings"] == 6        
    assert response.status_code == 200

def test_recipes_id(client):
    response_id = client.get('/recipes/65e9783df111ab6e7a864fa4')    
    data_id = json.loads(response_id.get_data(as_text=True))
    recipe_id = data_id
    assert recipe_id["_id"] == "65e9783df111ab6e7a864fa4"
    assert recipe_id["cuisine"] == "Indian"
    assert recipe_id["ingredients"] == "Chicken breast, yogurt, lemon juice, ginger, garlic, garam masala, cumin, paprika, tomato sauce, cream, butter, salt, cilantro"
    assert recipe_id["instructions"] == "1. Marinate chicken in yogurt, lemon juice, ginger, garlic, and spices. 2. Grill chicken until cooked through. 3. In a separate pan, simmer tomato sauce with cream and butter. 4. Add cooked chicken to the sauce and simmer for a few minutes. 5. Garnish with fresh cilantro and serve with rice or naan bread."
    assert recipe_id["name"] == "Chicken Tikka Masala"
    assert recipe_id["servings"] == 8        
    assert response_id.status_code == 200

def test_create_recipe(client):    
    new_recipe_data = {
        "name": "Chocolate Cake",
        "ingredients": ["1 cup sugar", "2 cups flour", "1 cup water", "2 eggs", "1 tbsp chocolate"],
        "instructions": "Mix ingredients, bake for 45 minutes at 350 degrees."
    }    
    response = client.post('/recipes', json=new_recipe_data)
    data = json.loads(response.data)    
    assert response.status_code == 201
    assert data['message'] == "Recipe created successfully"