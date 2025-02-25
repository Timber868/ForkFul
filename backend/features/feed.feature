Feature: View Feed of Recipes
  As a registered user
  I want to access the feed of recipes posted
  So that I can discover new and interesting dishes

  Scenario: Displaying a list of recipes
    Given the following recipes exist
      | name            | username | posted_date | ingredients                             | description                                                                        | image                |
      | Chocolate Cake  | Alice    | 2025-01-01  | Chocolate, Flour, Butter, Sugar, Milk   | A moist and decadent chocolate cake topped with creamy chocolate frosting.         | chocolate_cake.jpg   |
      | Vegan Salad     | Bob      | 2025-01-02  | Salad, Beets, Carrots, Vinaigrette      | A colorful salad loaded with greens, crunchy veggies, and a light vinaigrette.     | vegan_salad.jpg      |
    When the User tries to access the list of stored recipes
    Then the User should see a list of recipes
    And each recipe item should display the name, username, posted_date, ingredients, description, and image

  Scenario: Show a message when no recipes are available
    Given there are no recipes posted by other users
    When the User tries to access the list of recipes available
    Then the User should see an empty list of recipes

  Scenario: Warning for recipes with incomplete details when many recipes exist (Alternative Flow)
    Given the following recipes exist
      | name                 | username | posted_date | ingredients                                           | description                                                        | image.jpg                |
      | Mystery Dish         | Dana     | 2025-01-04  | Unknown                                               | A mystery dish whose content are Unknown.                          | mystery_dish.jpg         |
      | Spicy Tofu Stir Fry  | Eva      | 2025-01-05  | Tofu, Vegetables, Soy Sauce                           | A delicious spicy tofu stir fry with a kick of chili.              | spicy_tofu.jpg           |
      | Garlic Bread         | Frank    | 2025-01-06  | Bread, Garlic, Butter                                 | Perfectly crispy garlic bread to complement any meal.              | garlic_bread.jpg         |
      | Caesar Salad         | Grace    | 2025-01-07  | Romaine, Croutons, Caesar Dressing                    | Classic Caesar salad with a tangy dressing.                        | caesar_salad.jpg         |
      | Blueberry Muffins    | Henry    | 2025-01-08  | Blueberries, Flour, Sugar                             | Scrumptious blueberry muffins with bursts of fruit.                | blueberry_muffins.jpg    |
      | Avocado Toast        | Ivy      | 2025-01-09  | Avocado, Toast, Salt                                  | Trendy avocado toast perfect for a quick breakfast.                | avocado_toast.jpg        |
      | Pancakes             | Jack     | 2025-01-10  | Flour, Eggs, Milk                                     | Fluffy pancakes served with maple syrup.                           | pancakes.jpg             |
      | Fruit Smoothie       | Kelly    | 2025-01-11  | Mixed Fruits, Yogurt, Honey                           | Refreshing fruit smoothie to kickstart your day.                   | fruit_smoothie.jpg       |
      | Beef Tacos           | Liam     | 2025-01-12  | Beef, Tortillas, Salsa                                | Tasty beef tacos with a fresh salsa.                               | beef_tacos.jpg           |
      | Mushroom Risotto     | Mia      | 2025-01-13  | Mushrooms, Arborio Rice, White Wine                   | Creamy mushroom risotto with a rich umami flavor.                  | mushroom_risotto.jpg     |
      | Sushi Rolls          | Noah     | 2025-01-14  | Rice, Seaweed, Fish                                   | Fresh sushi rolls made with premium ingredients.                   | sushi_rolls.jpg          |
      | Chicken Curry        | Olivia   | 2025-01-15  | Chicken, Curry Powder, Rice                           | Aromatic chicken curry with a blend of spices.                     | chicken_curry.jpg        |
      | Vegan Burger         | Paul     | 2025-01-16  | Vegan Patty, Lettuce, Tomato                          | A hearty vegan burger with all the fixings.                        | vegan_burger.jpg         |
      | Eggplant Parmesan    | Quinn    | 2025-01-17  | Eggplant, Cheese, Tomato Sauce                        | Italian eggplant parmesan baked to perfection.                     | eggplant_parmesan.jpg    |
      | Fish and Chips       | Rachel   | 2025-01-18  | Fish, Potatoes, Batter                                | Crispy fish and chips with a side of tartar sauce.                 | fish_and_chips.jpg       |
      | Lentil Soup          | Steve    | 2025-01-19  | Lentils, Carrots, Celery, Onions                      | Warm and hearty lentil soup perfect for cold days.                 | lentil_soup.jpg          |
      | Strawberry Shortcake | Tina     | 2025-01-20  | Strawberries, Cream, Cake                             | Classic strawberry shortcake with fresh strawberries.              | strawberry_shortcake.jpg |
      | Quinoa Salad         | Uma      | 2025-01-21  | Quinoa, Mixed Vegetables, Lemon Dressing              | Nutritious quinoa salad with a zesty lemon dressing.               | quinoa_salad.jpg         |
      | Omelette             | Victor   | 2025-01-22  | Eggs, Cheese, Ham                                     | Quick and easy omelette with a mix of ingredients.                 | omelette.jpg             |
      | Chocolate Brownies   | Wendy    | 2025-01-23  | Chocolate, Flour, Butter, Sugar                       | Rich chocolate brownies with a fudgy center.                       | chocolate_brownies.jpg   |
    When the User tries to access the list of stored recipes
    Then the User should see all 20 recipes with no issues


