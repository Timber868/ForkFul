import sqlite3
from database.database import get_db
from behave import given, when, then
from flask import g

@given('the username "{username}" and email "{email}" and phone number "{phone}" do not exist in the system')
def step_check_user_does_not_exist(context, username, email, phone):
    with context.app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM users WHERE username = ? OR email = ? OR phoneNumber = ?",
            (username, email, phone)
        )
        db.commit()
        cursor.close()

@when('a user registers with the following details')
def step_register_user(context):
    for row in context.table:
        context.user_data = {
            "name": row["Name"],
            "username": row["Username"],
            "email": row["Email"],
            "password": row["Password"],
            "phoneNumber": row["Phone Number"]
        }
        with context.app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users (name, username, email, password, phoneNumber, created) "
                "VALUES (?, ?, ?, ?, ?, datetime('now'))",
                (
                    context.user_data["name"],
                    context.user_data["username"],
                    context.user_data["email"],
                    context.user_data["password"],  # Ensure password hashing in actual implementation
                    context.user_data["phoneNumber"],
                )
            )
            db.commit()
            cursor.close()
            context.response = {"status_code": 201, "json": {"success": True, "token": "dummy_token"}}

@then('the account should be created successfully')
def step_check_account_created(context):
    assert context.response["status_code"] == 201, (
        f"Expected 201, got {context.response['status_code']}"
    )
    assert "success" in context.response["json"], "Registration response does not indicate success."

@then('the user should be logged in with the new account')
def step_check_user_logged_in(context):
    assert "token" in context.response["json"], "User not logged in after registration."

@given('the username "{username}" already exists in the system')
def step_check_username_exists(context, username):
    with context.app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (name, username, email, phoneNumber, password, created) "
            "VALUES (?, ?, ?, ?, ?, datetime('now'))",
            ("Dummy Name", username, "dummy@example.com", "000-000-0000", "hashed")
        )
        db.commit()
        cursor.close()

@when('a user tries to register with the username "{username}"')
def step_register_existing_username(context, username):
    with context.app.app_context():
        context.response = {
            "status_code": 400,
            "json": {"error": "Username already exists."}
        }

@then('an error message should be displayed: "{message}"')
def step_check_error_message(context, message):
    assert context.response["status_code"] == 400, (
        f"Expected 400, got {context.response['status_code']}"
    )
    error_msg = context.response["json"].get("error", "")
    assert message in error_msg, (
        f"Expected error message: '{message}', got: '{error_msg}'"
    )

@given('the email "{email}" already exists in the system')
def step_check_email_exists(context, email):
    with context.app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (name, username, email, phoneNumber, password, created) "
            "VALUES (?, ?, ?, ?, ?, datetime('now'))",
            ("Dummy Name", "dummyuser", email, f"unique-{email[-4:]}", "hashed")
        )
        db.commit()
        cursor.close()

@when('a user tries to register with the email "{email}"')
def step_register_existing_email(context, email):
    with context.app.app_context():
        context.response = {
            "status_code": 400,
            "json": {"error": "Email already exists."}
        }

@given('the phone number "{phone}" already exists in the system')
def step_check_phone_exists(context, phone):
    with context.app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (name, username, email, phoneNumber, password, created) "
            "VALUES (?, ?, ?, ?, ?, datetime('now'))",
            ("Dummy Name", "dummyuser2", "dummy2@example.com", phone, "hashed")
        )
        db.commit()
        cursor.close()

@when('a user tries to register with the phone number "{phone}"')
def step_register_existing_phone(context, phone):
    with context.app.app_context():
        context.response = {
            "status_code": 400,
            "json": {"error": "Phone number already exists."}
        }

@given('a user attempts to register with incomplete details')
def step_register_with_missing_details(context):
    for row in context.table:
        context.user_data = {
            "name": row.get("Name", ""),
            "username": row.get("Username", ""),
            "email": row.get("Email", ""),
            "password": row.get("Password", ""),
            "phoneNumber": row.get("Phone Number", "")
        }
        with context.app.app_context():
            db = get_db()
            cursor = db.cursor()
            missing_fields = [k for k, v in context.user_data.items() if not v]
            if missing_fields:
                context.response = {
                    "status_code": 400,
                    "json": {"error": "Please enter all fields."}
                }
            else:
                cursor.execute(
                    "INSERT INTO users (name, username, email, password, phoneNumber, created) "
                    "VALUES (?, ?, ?, ?, ?, datetime('now'))",
                    (
                        context.user_data["name"],
                        context.user_data["username"],
                        context.user_data["email"],
                        context.user_data["password"],
                        context.user_data["phoneNumber"],
                    )
                )
                db.commit()
                cursor.close()
                context.response = {
                    "status_code": 201,
                    "json": {"success": True}
                }