Feature: Search a Recipe by Name

    As a user,
    I would like to search for a recipe by name,
    so that I can quickly locate a recipe that meets my needs.

    Scenario Outline: Successfully search for a recipe (Normal Flow)
        Given the following recipes exist
            | recipeName          | posted_date | ingredients                | username | description             | image                   |
            | Chocolate Cake      | 2025-01-01  | Flour, Sugar, Cocoa Powder | Alice    | Rich chocolate flavor   | chocolate_cake.jpg      |
            | Vegan Salad         | 2025-01-02  | Lettuce, Tomato, Cucumber  | Bob      | Fresh and healthy salad | vegan_salad.jpg         |
            | Spaghetti Carbonara | 2025-01-03  | Pasta, Eggs, Bacon         | Charlie  | Creamy and savory pasta | spaghetti_carbonara.png |
        When the user accesses the list of stored recipes named "Chocolate Cake"
        Then the User should see the following recipes
            | Chocolate Cake      | 2025-01-01  | Flour, Sugar, Cocoa Powder | Alice  | Rich chocolate flavor   | chocolate_cake.jpg |

    Scenario: Show an error message when no matching recipe is found (Error Flow)
        Given the following recipes exist
            | recipeName          | posted_date | ingredients                | username | description             | image            |
            | Chocolate Cake      | 2025-01-01  | Flour, Sugar, Cocoa Powder | Alice    | Rich chocolate flavor   | chocolate_cake.jpg|
            | Vegan Salad         | 2025-01-02  | Lettuce, Tomato, Cucumber  | Bob      | Fresh and healthy salad | vegan_salad.jpg   |
            | Spaghetti Carbonara | 2025-01-03  | Pasta, Eggs, Bacon         | Charlie  | Creamy and savory pasta | spaghetti_carbonara.png |
        When the user accesses the list of stored recipes named "Nonexistent Recipe"
        Then the User should see an error message "No recipes found for 'Nonexistent Recipe'"

    Scenario: Search using a partial recipe name (Alternate Flow)
        Given the following recipes exist
            | recipeName           | posted_date | ingredients                                          | username | description                    | image                         |
            | Chocolate Cake       | 2025-01-01  | Flour, Sugar, Cocoa Powder                           | Alice    | Rich chocolate flavor          | chocolate_cake.jpg            |
            | Vegan Salad          | 2025-01-02  | Lettuce, Tomato, Cucumber                            | Bob      | Fresh and healthy salad        | vegan_salad.jpg               |
            | Spaghetti Carbonara  | 2025-01-03  | Pasta, Eggs, Bacon                                   | Charlie  | Creamy and savory pasta        | spaghetti_carbonara.png       |
            | Spaghetti Bolognese  | 2025-01-04  | Pasta, Tomatoes, Ground Beef, Onion, Garlic          | Alice    | Classic Italian pasta dish     | spaghetti_bolognese.jpg       |
            | Spaghetti Puttanesca | 2025-01-05  | Pasta, Olives, Capers, Garlic, Tuna                  | Charlie  | Spicy and flavorful            | spaghetti_puttanesca.jpg      |
        When the user accesses the list of stored recipes named "Spaghetti"
        Then the User should see the following recipes
            | Spaghetti Carbonara  | 2025-01-03  | Pasta, Eggs, Bacon                                   | Charlie  | Creamy and savory pasta        | spaghetti_carbonara.png       |
            | Spaghetti Bolognese  | 2025-01-04  | Pasta, Tomatoes, Ground Beef, Onion, Garlic          | Alice    | Classic Italian pasta dish     | spaghetti_bolognese.jpg       |
            | Spaghetti Puttanesca | 2025-01-05  | Pasta, Olives, Capers, Garlic, Tuna                  | Charlie  | Spicy and flavorful            | spaghetti_puttanesca.jpg      |
