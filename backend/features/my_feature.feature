Feature: Flask API

  Scenario: Checking if the Flask app is running
    Given the Flask app is running
    When I send a GET request to "/"
    Then I should receive a 200 status code