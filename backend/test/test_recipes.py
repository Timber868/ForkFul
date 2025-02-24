import os
import pytest
from app import app
from database.database import get_db

# Ensure test directory exists
TEST_IMAGE_DIR = "tests/"
if not os.path.exists(TEST_IMAGE_DIR):
    os.makedirs(TEST_IMAGE_DIR)

# Create dummy test images
TEST_IMAGE_PATH = os.path.join(TEST_IMAGE_DIR, "test_image.jpg")
TEST_INVALID_IMAGE_PATH = os.path.join(TEST_IMAGE_DIR, "test_invalid.txt")
TEST_LARGE_IMAGE_PATH = os.path.join(TEST_IMAGE_DIR, "large_test_image.jpg")

# Generate test images if they don't exist
if not os.path.exists(TEST_IMAGE_PATH):
    with open(TEST_IMAGE_PATH, "wb") as f:
        f.write(os.urandom(1024))  # 1 KB dummy image

if not os.path.exists(TEST_INVALID_IMAGE_PATH):
    with open(TEST_INVALID_IMAGE_PATH, "w") as f:
        f.write("This is not an image file.")

if not os.path.exists(TEST_LARGE_IMAGE_PATH):
    with open(TEST_LARGE_IMAGE_PATH, "wb") as f:
        f.write(os.urandom(5 * 1024 * 1024))  # 5 MB dummy image

@pytest.fixture
def client():
    """Create a test client with a separate test database."""
    app.config["TESTING"] = True
    app.config["DATABASE"] = "tests/test_database.db"  # Use a separate DB for testing

    with app.test_client() as client:
        with app.app_context():
            db = get_db()
            db.execute("DELETE FROM recipes")  # Clear test data before running
            db.commit()
        yield client

# Normal Flow: Successful Recipe Submission
def test_create_recipe_success(client):
    """Test successful recipe creation with all valid fields."""
    data = {
        "name": "Chocolate Cake",
        "posted_date": "2025-02-20",
        "username": "testuser",
        "ingredients": "Flour, Sugar, Cocoa Powder",
        "description": "A delicious chocolate cake."
    }
    
    with open(TEST_IMAGE_PATH, "rb") as img:
        data["image"] = img
        response = client.post("/recipes/", data=data, content_type="multipart/form-data")

    assert response.status_code == 201
    assert response.json["message"] == "Recipe successfully created!"
    assert "id" in response.json["recipe"]

# Error Flow: Missing Required Fields (Using Parameterized Tests)
@pytest.mark.parametrize("missing_field", ["name", "posted_date", "username", "ingredients", "description"])
def test_create_recipe_missing_field(client, missing_field):
    """Test recipe creation with missing required fields."""
    data = {
        "name": "Chocolate Cake",
        "posted_date": "2025-02-20",
        "username": "testuser",
        "ingredients": "Flour, Sugar, Cocoa Powder",
        "description": "A delicious chocolate cake."
    }
    
    del data[missing_field]  # Remove one field

    with open(TEST_IMAGE_PATH, "rb") as img:
        data["image"] = img
        response = client.post("/recipes/", data=data, content_type="multipart/form-data")

    assert response.status_code == 400
    assert response.json["error"] == f"{missing_field} is required and cannot be empty"

# Error Flow: Invalid Date Format
def test_create_recipe_invalid_date(client):
    """Test recipe creation with an invalid date format."""
    data = {
        "name": "Chocolate Cake",
        "posted_date": "20-02-2025",  # Invalid format (should be YYYY-MM-DD)
        "username": "testuser",
        "ingredients": "Flour, Sugar, Cocoa Powder",
        "description": "A delicious chocolate cake."
    }
    
    with open(TEST_IMAGE_PATH, "rb") as img:
        data["image"] = img
        response = client.post("/recipes/", data=data, content_type="multipart/form-data")

    assert response.status_code == 400
    assert response.json["error"] == "Invalid date format. Use YYYY-MM-DD"

# Error Flow: No Image Uploaded
def test_create_recipe_no_image(client):
    """Test recipe creation without an image (should fail)."""
    data = {
        "name": "Chocolate Cake",
        "posted_date": "2025-02-20",
        "username": "testuser",
        "ingredients": "Flour, Sugar, Cocoa Powder",
        "description": "A delicious chocolate cake."
    }
    
    response = client.post("/recipes/", data=data, content_type="multipart/form-data")
    
    assert response.status_code == 400
    assert response.json["error"] == "No image uploaded"

# Error Flow: Invalid Image Format
def test_create_recipe_invalid_image_format(client):
    """Test recipe creation with an invalid image format."""
    data = {
        "name": "Chocolate Cake",
        "posted_date": "2025-02-20",
        "username": "testuser",
        "ingredients": "Flour, Sugar, Cocoa Powder",
        "description": "A delicious chocolate cake."
    }
    
    with open(TEST_INVALID_IMAGE_PATH, "rb") as img:
        data["image"] = img
        response = client.post("/recipes/", data=data, content_type="multipart/form-data")

    assert response.status_code == 400
    assert response.json["error"] == "Invalid file type. Allowed types: png, jpg, jpeg, gif"

# Edge Case: Extra Fields (Should Ignore Extra Data)
def test_create_recipe_extra_fields(client):
    """Test recipe creation with extra unexpected fields."""
    data = {
        "name": "Chocolate Cake",
        "posted_date": "2025-02-20",
        "username": "testuser",
        "ingredients": "Flour, Sugar, Cocoa Powder",
        "description": "A delicious chocolate cake.",
        "extra_field": "This should be ignored"  # Extra field
    }
    
    with open(TEST_IMAGE_PATH, "rb") as img:
        data["image"] = img
        response = client.post("/recipes/", data=data, content_type="multipart/form-data")

    assert response.status_code == 201
    assert response.json["message"] == "Recipe successfully created!"

# Edge Case: Large Image Upload (Limit Testing)
def test_create_recipe_large_image(client):
    """Test large image upload (limit testing)."""
    data = {
        "name": "Large Image Test",
        "posted_date": "2025-02-20",
        "username": "testuser",
        "ingredients": "Flour, Sugar, Cocoa Powder",
        "description": "Testing with a large image file."
    }
    
    with open(TEST_LARGE_IMAGE_PATH, "rb") as img:
        data["image"] = img
        response = client.post("/recipes/", data=data, content_type="multipart/form-data")

    assert response.status_code in [201, 400]  # Some servers may reject large uploads


# Error Flow: No Image Uploaded
def test_create_recipe_no_image(client):
    """Test recipe creation without an image"""
    data = {
        "name": "Chocolate Cake",
        "posted_date": "2025-02-20",
        "username": "testuser",
        "ingredients": "Flour, Sugar, Cocoa Powder",
        "description": "A delicious chocolate cake."
    }
    response = client.post("/recipes/", data=data, content_type="multipart/form-data")
    
    assert response.status_code == 400
    assert response.json["error"] == "No image uploaded"


# Test for get all recipes
def test_get_recipe_no_recipes(client):
    """Test getting all recipes when no recipes exist."""
    response = client.get("/recipes/")
    assert response.status_code == 200
    assert response.json == []

# Test for getting all receipes
def test_get_all_recipes(client):
    """Test getting all recipes."""
    data_recipe1 = {
        "name": "Chocolate Cake",
        "posted_date": "2025-02-20",
        "username": "testuser",
        "ingredients": "Flour, Sugar, Cocoa Powder",
        "description": "A delicious chocolate cake."
    }

    data_recipe2 = {
        "name": "Vegan Salad",
        "posted_date": "2025-02-21",
        "username": "testuser",
        "ingredients": "Lettuce, Tomatoes, Cucumbers",
        "description": "A healthy vegan salad."
    }

    #Add both recipes to the database
    with open(TEST_IMAGE_PATH, "rb") as img:
        data_recipe1["image"] = img
        response = client.post("/recipes/", data=data_recipe1, content_type="multipart/form-data")
        assert response.status_code == 201

    with open(TEST_IMAGE_PATH, "rb") as img:
        data_recipe2["image"] = img
        response = client.post("/recipes/", data=data_recipe2, content_type="multipart/form-data")
        assert response.status_code == 201

    response = client.get("/recipes/")
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["name"] == "Chocolate Cake"
    assert response.json[0]["posted_date"] == "2025-02-20"
    assert response.json[0]["username"] == "testuser"
    assert response.json[0]["ingredients"] == "Flour, Sugar, Cocoa Powder"
    assert response.json[0]["description"] == "A delicious chocolate cake."
    assert "image" in response.json[0]

    assert response.json[1]["name"] == "Vegan Salad"
    assert response.json[1]["posted_date"] == "2025-02-21"
    assert response.json[1]["username"] == "testuser"
    assert response.json[1]["ingredients"] == "Lettuce, Tomatoes, Cucumbers"
    assert response.json[1]["description"] == "A healthy vegan salad."
    assert "image" in response.json[1]
