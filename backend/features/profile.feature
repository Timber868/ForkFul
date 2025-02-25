Feature: View Profile Pages
  As a user,
  I want to view the profile page of other users or my own profile page,
  So that I can view the recipes posted by that user only.

  Scenario: View my own profile page
    Given I am a registered user
    And I am logged in
    When I look for my posted recipes
    Then the response status should be 200
    And I should see all the recipes I have posted

  Scenario: View another user's profile page
    Given I am a registered user
    And I am logged in
    And I am viewing another user's profile page
    When I look for the recipes posted by that user
    Then the response status should be 200
    And I should see all the recipes posted by that user
    And I should not see recipes from other users

  Scenario: Profile page shows user details
    Given I am a registered user
    And I am logged in
    And I am on a user's profile page
    When I look at the user details
    Then the response status should be 200
    And I should see the user's username, name, email, and phone number

  Scenario: No recipes available on user profile
    Given I am a registered user
    And I am logged in
    And I am on a user's profile page
    And the user has not posted any recipes
    When I look for the recipes posted by that user
    Then the response status should be 200
    And I should see the error message "No recipes posted yet."

  Scenario: Error handling for unavailable profile
    Given I am a registered user
    And I am logged in
    And I am trying to access a profile page that does not exist
    When I attempt to view the profile
    Then the response status should be 404
    And I should see the error message "This profile does not exist or is no longer available."