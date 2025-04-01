Feature: Search a Recipe by Name

  As a user,
  I would like to search for a recipe by name,
  so that I can quickly locate a recipe that meets my needs.

  Background:
    Given I am a registered user
    And I am logged in

  Scenario Outline: Successfully search for a recipe (Normal Flow)
    Given I am on the "Search Recipe" page
    When I enter the recipe name "<recipeName>" into the search field
    And I perform the search
    Then I should see a list of recipes with names containing "<recipeName>"
    And each recipe in the list should display the following fields:
      | name        |
      | posted_date |
      | ingredients |
      | username    |
      | description |
      | image       |

    Examples:
      | recipeName          | posted_date | ingredients                | username | description             | image                     |
      | Chocolate Cake      | 2025-01-01  | Flour, Sugar, Cocoa Powder | Alice    | Rich chocolate flavor   | chocolate_cake.jpg        |
      | Vegan Salad         | 2025-01-02  | Lettuce, Tomato, Cucumber  | Bob      | Fresh and healthy salad | vegan_salad.jpg           |
      | Spaghetti Carbonara | 2025-01-03  | Pasta, Eggs, Bacon         | Charlie  | Creamy and savory pasta | spaghetti_carbonara.png   |

  Scenario: Show an error message when no matching recipe is found (Error Flow)
    Given I am on the "Search Recipe" page
    When I enter the recipe name "Nonexistent Recipe" into the search field
    And I perform the search
    Then I should see an error message "No recipes found for 'Nonexistent Recipe'"

Scenario: Search using a partial recipe name (Alternate Flow)
  Given I am on the "Search Recipe" page
  When I search for the partial recipe name "cho"
  Then I should see a list of recipes where each recipe name starts with "cho"