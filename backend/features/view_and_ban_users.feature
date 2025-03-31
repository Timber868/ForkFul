Feature: View and Ban Users

  As an admin,
  I want to view a list of users and ban a specific user,
  so that I can restrict access for misbehaving users.

  Scenario: Successfully banning an active user (Normal Flow)
    Given the following users exist:
      | username    | email               | status  |
      | user123     | user123@test.com    | active  |
      | troubleUser | trouble@test.com    | active  |
      | goodUser    | good@test.com       | active  |
    When I ban the user with username "troubleUser"
    Then I should receive status code 200
    And the user with username "troubleUser" should have status "banned"
    And the user "troubleUser" should no longer have access to the application

  Scenario: Attempting to ban an already banned user (Error Flow)
    Given the following user exists:
      | username    | email               | status  |
      | troubleUser | trouble@test.com    | banned  |
    When I ban the user with username "troubleUser"
    Then I should receive status code 400
    And I should receive an error message "User is already banned"
    And the user's status remains "banned"

  Scenario: Viewing the list of users (Alternative Flow)
    Given the following users exist:
      | username | email            | status |
      | user1    | user1@test.com   | active |
      | user2    | user2@test.com   | banned |
      | user3    | user3@test.com   | active |
    When I request the list of users
    Then I should receive status code 200
    And I should see the following users:
      | username | email            | status |
      | user1    | user1@test.com   | active |
      | user2    | user2@test.com   | banned |
      | user3    | user3@test.com   | active |
