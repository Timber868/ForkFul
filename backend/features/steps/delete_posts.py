import sqlite3
from behave import given, when, then
from database.database import get_db
from flask import g

@given('I am an authenticated admin user')
def step_impl_admin_authenticated(context):
    # For testing purposes, we assume the admin user is authenticated.
    # Authentication logic is assumed to be handled by middleware/decorators.
    context.admin_authenticated = True

@given('a recipe with ID "{recipe_id}" exists')
def step_impl_recipe_exists(context, recipe_id):
    # Store the recipe_id for later steps
    context.recipe_id = recipe_id
    with context.app.app_context():
        db = get_db()
        cursor = db.cursor()
        # Ensure a clean state by deleting any existing record with this ID
        cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        # Insert a dummy recipe with the specified ID.
        # This assumes that your recipes table allows manual insertion of the ID.
        cursor.execute(
            "INSERT INTO recipes (id, name, posted_date, username, ingredients, description, image) "
            "VALUES (?, ?, date('now'), ?, ?, ?, ?)",
            (recipe_id, "Test Recipe", "admin", "Test ingredients", "Test description", "static/uploads/test.jpg")
        )
        db.commit()
        cursor.close()

@given('no recipe exists with ID "{recipe_id}"')
def step_impl_recipe_not_exists(context, recipe_id):
    # Store the recipe_id for later steps
    context.recipe_id = recipe_id
    with context.app.app_context():
        db = get_db()
        cursor = db.cursor()
        # Ensure that the recipe does not exist in the database
        cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        db.commit()
        cursor.close()

@when('I request to delete the recipe with ID "{recipe_id}"')
def step_impl_request_delete_recipe(context, recipe_id):
    # Ensure we have the correct recipe_id stored
    context.recipe_id = recipe_id
    # Use the Flask test client to send a DELETE request to the endpoint
    response = context.client.delete(f"/recipes/{recipe_id}")
    context.response = response

@then('the recipe should be removed from the system')
def step_impl_check_recipe_removed(context):
    with context.app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM recipes WHERE id = ?", (context.recipe_id,))
        recipe = cursor.fetchone()
        cursor.close()
        assert recipe is None, f"Expected recipe with ID {context.recipe_id} to be removed, but it still exists."

@then('the system should return a success response')
def step_impl_check_success_response(context):
    # Check that the response status code is 200 and the expected message is returned.
    assert context.response.status_code == 200, (
        f"Expected status code 200, got {context.response.status_code}"
    )
    json_data = context.response.get_json()
    assert json_data.get("message") == "Recipe successfully deleted!", (
        f"Expected success message 'Recipe successfully deleted!', got '{json_data.get('message')}'"
    )

@then('the system should return an error response "Recipe not found"')
def step_impl_check_error_response(context):
    # Check that the response status code is 404 and the error message is returned.
    assert context.response.status_code == 404, (
        f"Expected status code 404, got {context.response.status_code}"
    )
    json_data = context.response.get_json()
    assert "error" in json_data, "Expected error message in response"
    assert json_data["error"] == "Recipe not found", (
        f"Expected error 'Recipe not found', got '{json_data['error']}'"
    )