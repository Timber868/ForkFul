from behave import given, when, then

@given('I am on the login page')
def step_on_login_page(context):
    # Set up context or perform actions that simulate being on the login page
    context.current_page = "login"

@when('I enter valid credentials')
def step_enter_valid_credentials(context):
    # Simulate entering valid credentials (e.g., username: "test", password: "1234")
    context.login_successful = True  # Example result after checking credentials

@when('I enter invalid credentials')
def step_enter_invalid_credentials(context):
    # Simulate entering invalid credentials
    context.login_successful = False

@then('I should see a welcome message')
def step_check_welcome_message(context):
    assert context.login_successful, "Expected successful login but it failed."

@then('I should see an error message')
def step_check_error_message(context):
    assert not context.login_successful, "Expected login to fail but it succeeded."