from behave import given, when, then

@given("I have a registered account")
def step_registered_account(context):
    context.username = "admin"

@given("I provide valid username and password")
def step_valid_credentials(context):
    context.password = "password"

@given("I provide valid username but an incorrect password")
def step_invalid_credentials(context):
    context.password = "wrong_password"

@given("I have incomplete login details")
def step_incomplete_details(context):
    if hasattr(context, 'username'):
        del context.username
    if hasattr(context, 'password'):
        del context.password

@given("I am logged in")
def step_logged_in(context):
    context.username = "admin"
    context.password = "password"
    payload = {"username": context.username, "password": context.password}
    response = context.client.post('/auth/login', json=payload)
    assert response.status_code == 200, "Failed to log in."
    context.response = response

@when("I send a login request")
def step_send_login(context):
    payload = {}
    if hasattr(context, 'username') and context.username is not None:
        payload["username"] = context.username
    if hasattr(context, 'password') and context.password is not None:
        payload["password"] = context.password
    context.response = context.client.post('/auth/login', json=payload)

@when("I send a logout request")
def step_send_logout(context):
    context.response = context.client.post('/auth/logout')

@then('the response status should be {status_code:d}')
def step_check_status_code(context, status_code):
    actual = context.response.status_code
    assert actual == status_code, f"Expected status {status_code}, got {actual}"

@then('the response message should be "{message}"')
def step_check_message(context, message):
    json_data = context.response.get_json()
    actual = json_data.get("message")
    assert actual == message, f"Expected message '{message}', got '{actual}'"