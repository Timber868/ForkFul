from behave import given, when, then
import os
from io import BytesIO
from features.steps.login_steps import step_check_status_code, step_check_message  # Import shared steps

BASE_URL = "/recipes"

# Helper function to ensure test files exist
def ensure_test_image_exists(image_path):
    """Ensure that the test image or file exists to prevent FileNotFoundError."""
    os.makedirs(os.path.dirname(image_path), exist_ok=True)  # Create directory if it doesn’t exist
    if not os.path.exists(image_path):
        with open(image_path, "wb") as f:
            if image_path.endswith((".jpg", ".jpeg", ".png", ".gif")):
                # Write a minimal valid JPEG header for testing
                f.write(b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00")
            else:
                f.write(b"This is a dummy file.")  # For invalid formats

@given("I am a registered user")
def step_registered_user(context):
    context.username = "testuser"

@given("I provide valid recipe details")
def step_fill_base_recipe(context):
    """Provide a base valid recipe for scenarios that modify specific fields."""
    context.recipe = {
        "name": "Test Recipe",
        "posted_date": "2025-02-20",
        "username": context.username,
        "ingredients": "Ingredient1, Ingredient2",
        "description": "A test recipe."
    }
    context.image_path = "tests/test_image.jpg"
    ensure_test_image_exists(context.image_path)

@given("I provide a valid recipe name, posted date, ingredients, username, description, and an image")
def step_fill_valid_recipe(context):
    context.recipe = {
        "name": "Chocolate Cake",
        "posted_date": "2025-02-20",
        "username": context.username,
        "ingredients": "Flour, Sugar, Cocoa Powder",
        "description": "A delicious chocolate cake."
    }
    context.image_path = "tests/test_image.jpg"
    ensure_test_image_exists(context.image_path)

@given("I provide incomplete recipe details with missing required fields")
def step_fill_incomplete_recipe(context):
    context.recipe = {
        "name": "",  # Missing required field
        "posted_date": "2025-02-20",
        "username": context.username,
        "ingredients": "Flour, Sugar, Cocoa Powder",
        "description": "A delicious chocolate cake."
    }
    context.image_path = "tests/test_image.jpg"
    ensure_test_image_exists(context.image_path)

@given("I provide a date that is not in the format 'YYYY-MM-DD'")
def step_invalid_date_format(context):
    context.recipe = {
        "name": "Fish Curry",
        "posted_date": "20-02-2025",  # Invalid format
        "username": context.username,
        "ingredients": "Fish, Coconut Milk",
        "description": "Authentic fish curry."
    }
    context.image_path = "tests/test_image.jpg"
    ensure_test_image_exists(context.image_path)

@given('I upload an image that is not in PNG, JPG, JPEG, or GIF format')
def step_invalid_image_format(context):
    context.recipe = {  # Ensure recipe is set even for invalid image case
        "name": "Test Recipe",
        "posted_date": "2025-02-20",
        "username": context.username,
        "ingredients": "Ingredient1, Ingredient2",
        "description": "A test recipe."
    }
    context.image_path = "tests/invalid_file.xyz"  # Invalid extension
    ensure_test_image_exists(context.image_path)

@given("I do not provide an image file")
def step_no_image_uploaded(context):
    context.recipe = {
        "name": "Test Recipe",
        "posted_date": "2025-02-20",
        "username": context.username,
        "ingredients": "Ingredient1, Ingredient2",
        "description": "A test recipe."
    }
    context.image_path = None

@when("I send a recipe submission request")
def step_submit_recipe(context):
    if not hasattr(context, "recipe"):
        raise AttributeError("context.recipe is missing. Ensure that you set up the recipe in a previous step.")

    # Prepare form data
    data = {
        "name": context.recipe["name"],
        "posted_date": context.recipe["posted_date"],
        "username": context.recipe["username"],
        "ingredients": context.recipe["ingredients"],
        "description": context.recipe["description"]
    }

    # Handle image file if provided
    if context.image_path:
        with open(context.image_path, "rb") as img_file:
            image_content = img_file.read()
        # Use BytesIO to keep the file content in memory
        data["image"] = (BytesIO(image_content), os.path.basename(context.image_path), "application/octet-stream")
    else:
        data["image"] = None  # No image case

    # Send the request with multipart/form-data
    response = context.client.post(
        BASE_URL + "/",
        data=data,  # Combine form fields and file
        headers=context.auth_headers,  # Include JWT Authorization
        content_type="multipart/form-data"  # Ensure correct content type
    )

    # Debugging output
    try:
        json_data = response.get_json()
        print("🔍 Backend Response:", response.status_code, json_data)
    except Exception as e:
        print("🔍 Backend Response (Raw):", response.status_code, response.data.decode(), f"Error: {e}")

    # Ensure response is stored correctly
    context.response = response
    print(f"🔍 Stored context.response: {context.response.status_code}")

@then("the response message should specify the missing required field")
def step_missing_field_error(context):
    json_data = context.response.get_json()
    assert "error" in json_data, "Error message not found"
    assert "is required" in json_data["error"], f"Unexpected error message: {json_data['error']}"




