Feature: Post a Recipe
  As a user,
  I want to post a recipe with a name, posted date, ingredient list, username, description, and an image,
  So that other users can view it on their feed.

  Scenario: Successfully post a new recipe with valid details
    Given I am a registered user
    And I am logged in
    And I provide a valid recipe name, posted date, ingredients, username, description, and an image
    When I send a recipe submission request
    Then the response status should be 201
    And the response message should be "Recipe successfully created!"

  Scenario: Recipe submission fails with missing required fields
    Given I am a registered user
    And I am logged in
    And I provide incomplete recipe details with missing required fields
    When I send a recipe submission request
    Then the response status should be 400
    And the response message should specify the missing required field

  Scenario: Recipe submission fails with an invalid date format
    Given I am a registered user
    And I am logged in
    And I provide a date that is not in the format 'YYYY-MM-DD'
    When I send a recipe submission request
    Then the response status should be 400
    And the response message should be "Invalid date format. Use YYYY-MM-DD"

  Scenario: Recipe submission fails with an invalid image format
    Given I am a registered user
    And I am logged in
    And I provide valid recipe details
    And I upload an image that is not in PNG, JPG, JPEG, or GIF format
    When I send a recipe submission request
    Then the response status should be 400
    And the response message should be "Invalid file type. Allowed types: png, jpg, jpeg, gif"

  Scenario: Recipe submission fails when no image is uploaded
    Given I am a registered user
    And I am logged in
    And I provide valid recipe details
    And I do not provide an image file
    When I send a recipe submission request
    Then the response status should be 400
    And the response message should be "No image uploaded"


