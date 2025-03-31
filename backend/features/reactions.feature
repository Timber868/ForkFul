Feature: React to a Recipe Post  
  As a user,  
  I want to react to a recipe post with a BOOM or a DOOM,  
  So that I can express how I feel about the recipe to the poster.  

  Background:  
    Given I am a registered user  
    And I am logged in  
    And a recipe post exists  

  Scenario Outline: Successfully react to a recipe post  
    Given I have not reacted to the post before  
    When I react to the post with "<reaction>"  
    Then the reaction "<reaction>" should be recorded for the post  
    And the total reaction count should be updated  

    Examples:  
      | reaction |  
      | BOOM     |  
      | DOOM     |  

  Scenario: Change my reaction on a recipe post  
    Given I have already reacted to the post with "BOOM"  
    When I change my reaction to "DOOM"  
    Then my reaction should be updated to "DOOM"  
    And the reaction count should reflect the change  

  Scenario: Remove my reaction from a recipe post  
    Given I have already reacted to the post with "DOOM"  
    When I remove my reaction  
    Then the reaction should be removed from the post  
    And the total reaction count should be updated  

  Scenario: View reactions on a recipe post  
    Given multiple users have reacted to the post  
    When I view the post  
    Then I should see the total number of BOOM and DOOM reactions  
