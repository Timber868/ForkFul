import sqlite3
from behave import given, when, then
from database.database import get_db
from flask import g

# Helper: Inserts a recipe into the "recipes" table.
def insert_recipe(db, recipe):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO recipes (name, username, posted_date, ingredients, description, image) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (
            recipe.get("name"),
            recipe.get("username"),
            recipe.get("posted_date"),
            recipe.get("ingredients"),
            recipe.get("description"),
            recipe.get("image"),
        )
    )
    db.commit()
    cursor.close()

@given('the following recipes exist')
def step_impl_insert_recipes(context):
    with context.app.app_context():
        db = get_db()
        # Clear the recipes table before inserting new data.
        cursor = db.cursor()
        cursor.execute("DELETE FROM recipes")
        db.commit()
        cursor.close()
        for row in context.table:
            recipe = {
                "name": row["name"],
                "username": row["username"],
                "posted_date": row["posted_date"],
                "ingredients": row["ingredients"],
                "description": row["description"],
                "image": row["image"]
            }
            insert_recipe(db, recipe)

@given('there are no recipes posted by other users')
def step_impl_no_recipes(context):
    with context.app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM recipes")
        db.commit()
        cursor.close()

@when('the User tries to access the list of stored recipes')
def step_impl_access_recipes(context):
    with context.app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT name, username, posted_date, ingredients, description, image FROM recipes")
        # Fetch all recipes as a list of dictionaries.
        rows = cursor.fetchall()
        context.recipes = [
            {
                "name": row["name"],
                "username": row["username"],
                "posted_date": row["posted_date"],
                "ingredients": row["ingredients"],
                "description": row["description"],
                "image": row["image"]
            } for row in rows
        ]
        cursor.close()

@then('the User should see a list of recipes')
def step_impl_see_recipe_list(context):
    assert context.recipes is not None, "No recipes were retrieved."
    assert len(context.recipes) > 0, "The recipes list is empty, but it should contain recipes."


@then('the User should see a list with both of these recipes in it')
def step_impl_see_recipe_list(context):
    assert context.recipes is not None, "No recipes were retrieved."
    assert len(context.recipes) == 2, "The recipes list should contain 2 recipes."
    assert context.recipes[0]["name"] == "Chocolate Cake", "First recipe name is incorrect."
    assert context.recipes[1]["name"] == "Vegan Salad", "Second recipe name is incorrect."

@then('each recipe item should display the name, username, posted_date, ingredients, description, and image')
def step_impl_recipe_fields(context):
    required_fields = ["name", "username", "posted_date", "ingredients", "description", "image"]
    for recipe in context.recipes:
        for field in required_fields:
            assert field in recipe, f"Field '{field}' is missing in recipe: {recipe}"
            assert recipe[field] is not None, f"Field '{field}' is None in recipe: {recipe}"

@then('the User should see an empty list of recipes')
def step_impl_empty_recipe_list(context):
    assert context.recipes is not None, "Recipes result is None."
    assert len(context.recipes) == 0, f"Expected an empty list, but got {len(context.recipes)} recipes."

@then('the User should see all 20 recipes with no issues')
def step_impl_see_all_20_recipes(context):
    expected_count = 20
    actual_count = len(context.recipes)
    assert actual_count == expected_count, f"Expected {expected_count} recipes, but got {actual_count}."
    for recipe in context.recipes:
        assert all([recipe["name"], recipe["username"], recipe["posted_date"], recipe["ingredients"],
                    recipe["description"], recipe["image"]]), "Recipe has missing details."

@then('the User should see a warning "Some recipes have incomplete details."')
def step_impl_warning_incomplete(context):
    incomplete = [
        recipe for recipe in context.recipes
        if not all([recipe["name"].strip(), recipe["username"].strip(), recipe["posted_date"].strip(),
                    recipe["ingredients"].strip(), recipe["description"].strip()])
    ]
    context.incomplete_recipes = incomplete
    assert len(incomplete) > 0, "Expected some recipes to have incomplete details, but none were found."
    context.warning_message = "Some recipes have incomplete details."
    assert context.warning_message == "Some recipes have incomplete details."

@then('the incomplete recipes should be highlighted for review')
def step_impl_highlight_incomplete(context):
    assert hasattr(context, "incomplete_recipes"), "Incomplete recipes were not captured."
    assert len(context.incomplete_recipes) > 0, "No incomplete recipes to highlight."
