import sqlite3
from behave import given, when, then
from database.database import get_db
from flask import g
from urllib.parse import quote
import json

##Given was already defined in the feed steps

@when('the user accesses the list of stored recipes named "{recipe_name}"')
def step_impl_access_recipes(context, recipe_name):
    encoded_recipe_name = quote(recipe_name)
    with context.app.app_context():
        context.response = context.client.get(f'/recipes/{encoded_recipe_name}')

@then('the User should see the following recipes')
def step_impl_verify_specific_recipe(context):
    expected_recipes = context.table.rows

    response_data = json.loads(context.response.data)

    # Ensure exactly one recipe is returned
    assert len(response_data) == (len(expected_recipes) + 1 ), f"Expected {len(expected_recipes)} recipes, but found {len(response_data)}."

    actual_recipes = response_data
    for expected_row, actual_recipe in zip(actual_recipes, response_data):
        assert actual_recipe['name'] == expected_row['name'], \
            f"Expected recipe name '{expected_row['recipeName']}', found '{actual_recipe['name']}'."
        
        assert actual_recipe['posted_date'] == expected_row['posted_date'], \
            f"Expected posted date '{expected_row['posted_date']}', found '{actual_recipe['posted_date']}'."
        
        assert actual_recipe['ingredients'] == expected_row['ingredients'], \
            f"Expected ingredients '{expected_row['ingredients']}', found '{actual_recipe['ingredients']}'."
        
        assert actual_recipe['username'] == expected_row['username'], \
            f"Expected username '{expected_row['username']}', found '{actual_recipe['username']}'."
        
        assert actual_recipe['description'] == expected_row['description'], \
            f"Expected description '{expected_row['description']}', found '{actual_recipe['description']}'."
        
        assert actual_recipe['image'] == expected_row['image'], \
            f"Expected image '{expected_row['image']}', found '{actual_recipe['image']}'."

@then('the User should see an error message "{error_message}"')
def step_impl_verify_error_message(context, error_message):
    response_data = json.loads(context.response.data)

    assert 'error' in response_data, \
        f"Expected an error message in response but found none. Response was: {response_data}"

    assert response_data['error'] == error_message, \
        f"Expected error message '{error_message}', but found '{response_data['error']}'."