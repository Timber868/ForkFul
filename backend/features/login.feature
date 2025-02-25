Feature: User Login
  As a user,
  I want to log into my account,
  So that I can access the app features.

  Scenario: Successful login with valid credentials
    Given I have a registered account
    And I provide valid username and password
    When I send a login request
    Then the response status should be 200
    And the response message should be "Logged in successfully."

  Scenario: Login fails with incorrect password
    Given I have a registered account
    And I provide valid username but an incorrect password
    When I send a login request
    Then the response status should be 401
    And the response message should be "Invalid username or password."

  Scenario: Login fails with missing credentials
    Given I have incomplete login details
    When I send a login request
    Then the response status should be 400
    And the response message should be "Please enter both email and password."

  Scenario: Log out from the app
    Given I am logged in
    When I send a logout request
    Then the response status should be 200
    And the response message should be "Logged out successfully."
