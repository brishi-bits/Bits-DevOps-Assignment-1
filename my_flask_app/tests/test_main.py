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