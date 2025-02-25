Feature: User login

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter valid credentials
    Then I should see a welcome message

  Scenario: Unsuccessful login with invalid credentials
    Given I am on the login page
    When I enter invalid credentials
    Then I should see an error message