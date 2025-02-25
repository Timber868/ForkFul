from behave import given, when, then

@given("the Flask app is running")
def step_flask_running(context):
    assert context.client is not None  # Ensure client is set up

@when('I send a GET request to "{endpoint}"')
def step_send_get_request(context, endpoint):
    context.response = context.client.get(endpoint)

@then('I should receive a {status_code:d} status code')
def step_check_status_code(context, status_code):
    assert context.response.status_code == status_code, \
        f"Expected {status_code}, got {context.response.status_code}"
    