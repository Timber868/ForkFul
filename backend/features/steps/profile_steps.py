from behave import given, when, then

#All givens
@given("I am viewing another user's profile page")
def step_view_other_profile(context):
    context.username = "other"

@given("I am on a user's profile page")
def step_profile_page(context):
    context.username = "admin"

@given("I am trying to access a profile page that does not exist")
def step_user_not_exist(context):
    context.username = "fake"

@given("The user has not posted any recipes")
def step_no_recipes(context):
    context.username = "empty"

#All whens
@when("I look for my posted recipes")
def step_look_for_recipes(context):
    context.response = context.client.get('/profile/{}'.format(context.username))

@when("I look for the recipes posted by that user")
def step_look_for_other_recipes(context):
    context.response = context.client.get('/profile/{}'.format(context.username))

@when("I look at the user details")
def step_look_user_details(context):
    context.response = context.client.get('/profile/{}'.format(context.username))

@when("I attempt to view the profile")
def step_attemp_view_profile(context):
    context.response = context.client.get('/profile/{}'.format(context.username))


#All thens
@then("I should see all the recipes I have posted")
def step_check_own_recipes(context):
    data = context.response.json
    assert "recipes" in data, "No recipes key in response"
    assert all(recipe["username"] == context.username for recipe in data["recipes"]), \
        "Not all recipes belong to the logged-in user"

@then("I should see all the recipes posted by that user")
def step_check_other_user_recipes(context):
    data = context.response.json
    assert "recipes" in data, "No recipes key in response"
    assert all(recipe["username"] == context.otherUsername for recipe in data["recipes"]), \
        "Not all recipes belong to the viewed user"

@then("I should not see recipes from other users")
def step_check_no_unrelated_recipes(context):
    data = context.response.json
    assert "recipes" in data, "No recipes key in response"
    assert all(recipe["username"] == context.otherUsername for recipe in data["recipes"]), \
        "Found recipes from unrelated users"

@then("I should see the user's username, name, email, and phone number")
def step_check_user_details(context):
    data = context.response.json
    user = data['user']
    assert "username" in user, "Username is missing"
    assert "name" in user, "Bio is missing"
    assert "email" in user, "Profile picture is missing"
    assert "phoneNumber" in user, "Phone number is missing"

@then('I should see the error message "No recipes posted yet."')
def step_check_no_recipes_message(context):
    data = context.response.json
    assert "message" in data, "No message key in response"
    assert data["message"] == "No recipes posted yet.", \
        f"Expected 'No recipes posted yet.', got {data['message']}"

@then('I should see the error message "This profile does not exist or is no longer available."')
def step_check_profile_not_found_message(context):
    data = context.response.json
    assert "message" in data, "No message key in response"
    assert data["message"] == "This profile does not exist or is no longer available.", \
        f"Expected 'This profile does not exist or is no longer available.', got {data['message']}"

#Example then 
@then('I should receive a {status_code:d} status code')
def step_check_status_code(context, status_code):
    assert context.response.status_code == status_code, \
        f"Expected {status_code}, got {context.response.status_code}"
    
