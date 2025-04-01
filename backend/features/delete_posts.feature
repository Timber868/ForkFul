Feature: Delete a Recipe
  As an admin,
  I would like to delete a recipe,
  So that I can remove inappropriate recipes.

  Background:
    Given I am an authenticated admin user

  Scenario Outline: Successfully delete a recipe
    Given a recipe with ID "<recipe_id>" exists
    When I request to delete the recipe with ID "<recipe_id>"
    Then the recipe should be removed from the system
    And the system should return a success response

    Examples:
      | recipe_id |
      | 101       |
      | 202       |
      | 303       |

  Scenario Outline: Attempt to delete a non-existent recipe
    Given no recipe exists with ID "<recipe_id>"
    When I request to delete the recipe with ID "<recipe_id>"
    Then the system should return an error response "Recipe not found"

    Examples:
      | recipe_id |
      | 999       |