Feature: URL Shortener Functionality

  Scenario: Load the URL shortener page
    When I visit the URL shortener page
    Then I should see the URL input form

  Scenario: Submit a URL
    Given I am on the URL shortener page
    When I enter "https://www.example.com" into the URL input
    And I submit the form
    Then I should see a result

  Scenario: Enter an invalid input
    Given I am on the URL shortener page
    When I enter "not a url" into the URL input
    Then I should see a validation message