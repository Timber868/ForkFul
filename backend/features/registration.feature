Feature: User Registration

  Scenario: Successful account registration
    Given the username "new_user" and email "new_user@example.com" and phone number "123-456-0978" do not exist in the system
    When a user registers with the following details:
      | Name      | Username  | Email                  | Password  | Phone Number  |
      | John Doe  | new_user  | new_user@example.com   | Pass123!  | 123-456-0978  |
    Then the account should be created successfully
    And the user should be logged in with the new account

  Scenario: Registration fails when username already exists
    Given the username "existing_user" already exists in the system
    When a user tries to register with the username "existing_user"
    Then an error message should be displayed: "Username already exists."

  Scenario: Registration fails when email already exists
    Given the email "existing_email@example.com" already exists in the system
    When a user tries to register with the email "existing_email@example.com"
    Then an error message should be displayed: "Email already exists."

  Scenario: Registration fails when phone number already exists
    Given the phone number "123-456-0987" already exists in the system
    When a user tries to register with the phone number "123-456-0987"
    Then an error message should be displayed: "Phone number already exists."

  Scenario: Registration fails when required fields are missing
    Given a user attempts to register with incomplete details:
      | Name  | Username | Email                 | Password | Phone Number |
      |       | new_user | new_user@example.com  | Pass123! | 123-456-7891 |
    Then an error message should be displayed: "Please enter all fields."
