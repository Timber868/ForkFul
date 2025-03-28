from behave import given, when, then
from database.database import get_db
import random

# Helper functions to work with users.
def insert_user(db, user):
    cursor = db.cursor()
    # Provide dummy values for required fields not provided by the test.
    phoneNumber = user.get("phoneNumber", f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}")
    name = user.get("name", "Dummy Name")
    password = user.get("password", "dummy_password")
    cursor.execute(
        "INSERT INTO users (username, email, phoneNumber, name, password, status, created) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))",
        (user["username"], user["email"], phoneNumber, name, password, user["status"])
    )
    db.commit()
    cursor.close()

def get_user_by_username(db, username):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    cursor.close()
    return user

@given('the following users exist')
def step_given_users_exist(context):
    """
    Clears the users table and inserts the users provided in the table.
    Expected columns: username, email, and status.
    """
    with context.app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM users")
        db.commit()
        cursor.close()
        for row in context.table:
            user = {
                "username": row["username"],
                "email": row["email"],
                "status": row["status"]
            }
            insert_user(db, user)

@given('the following user exists')
def step_given_single_user_exists(context):
    """
    Inserts a single user using the table provided.
    Expected columns: username, email, and status.
    """
    with context.app.app_context():
        db = get_db()
        for row in context.table:
            user = {
                "username": row["username"],
                "email": row["email"],
                "status": row["status"]
            }
            insert_user(db, user)
            context.username = row["username"]

@when('I ban the user with username "{username}"')
def step_when_ban_user(context, username):
    """
    Retrieves the user id by username and sends a PUT request to ban that user.
    """
    with context.app.app_context():
        db = get_db()
        user = get_user_by_username(db, username)
        assert user is not None, f"User {username} not found"
        user_id = user["id"]
    context.response = context.client.put(f"/users/{user_id}/ban")

@when('I request the list of users')
def step_when_request_users(context):
    context.response = context.client.get("/users/")

@then('I should receive status code {status_code:d}')
def step_then_status_code(context, status_code):
    assert context.response.status_code == status_code, (
        f"Expected status code {status_code}, got {context.response.status_code}"
    )

@then('the user with username "{username}" should have status "{expected_status}"')
def step_then_user_status(context, username, expected_status):
    with context.app.app_context():
        db = get_db()
        user = get_user_by_username(db, username)
        assert user is not None, f"User {username} not found"
        actual_status = user["status"]
        assert actual_status == expected_status, (
            f"Expected status '{expected_status}' for user {username}, got '{actual_status}'"
        )

@then('I should receive an error message "{message}"')
def step_then_error_message(context, message):
    json_data = context.response.get_json()
    error = json_data.get("error")
    # Trim trailing period (if any) for comparison
    assert error.rstrip('.') == message, f"Expected error message '{message}', got '{error}'"

@then('the user "{username}" should no longer have access to the application')
def step_then_no_access(context, username):
    """
    Simulates a login attempt for the banned user. The login endpoint should return a 403 status.
    """
    payload = {"username": username, "password": "dummy_password"}  # using the dummy password
    login_response = context.client.post("/auth/login", json=payload)
    assert login_response.status_code == 403, (
        f"Expected 403 for banned user, got {login_response.status_code}"
    )

@then('the user\'s status remains "banned"')
def step_then_status_remains_banned(context):
    """
    Verifies that the user (stored in context.username) remains banned.
    """
    username = context.username
    with context.app.app_context():
        db = get_db()
        user = get_user_by_username(db, username)
        assert user is not None, f"User {username} not found"
        assert user["status"] == "banned", (
            f"User {username} status is '{user['status']}', expected 'banned'"
        )

@then('I should see the following users')
def step_then_verify_users_list(context):
    """
    Compares the list of users returned by the GET /users endpoint with the expected table.
    Expected columns: username, email, and status.
    """
    json_data = context.response.get_json()
    # Filter returned data to only the required fields.
    returned_users = [
        {"username": u["username"], "email": u["email"], "status": u["status"]}
        for u in json_data
    ]
    # Use as_dict() for each row so that behave correctly converts the table row to a dictionary.
    expected_users = [row.as_dict() for row in context.table]
    returned_sorted = sorted(returned_users, key=lambda x: x["username"])
    expected_sorted = sorted(expected_users, key=lambda x: x["username"])
    assert len(returned_sorted) == len(expected_sorted), (
        f"Expected {len(expected_sorted)} users, got {len(returned_sorted)}"
    )
    for expected, actual in zip(expected_sorted, returned_sorted):
        assert expected["username"] == actual["username"], (
            f"Expected username '{expected['username']}', got '{actual['username']}'"
        )
        assert expected["email"] == actual["email"], (
            f"Expected email '{expected['email']}', got '{actual['email']}'"
        )
        assert expected["status"] == actual["status"], (
            f"Expected status '{expected['status']}', got '{actual['status']}'"
        )
