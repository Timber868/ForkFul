# Normal Flow
def test_login_success(client):
    response = client.post('/auth/login', json={
        'username': 'admin',
        'password': 'password'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Logged in successfully.'

# Feature: React to a Recipe Post  
#   As a user,  
#   I want to react to a recipe post with a BOOM or a DOOM,  
#   So that I can express how I feel about the recipe to the poster.  

#   Background:  
#     Given I am a registered user  
#     And I am logged in  
#     And a recipe post exists  

#   Scenario Outline: Successfully react to a recipe post  
#     Given I have not reacted to the post before  
#     When I react to the post with "<reaction>"  
#     Then the reaction "<reaction>" should be recorded for the post  
#     And the total reaction count should be updated  

#     Examples:  
#       | reaction |  
#       | BOOM     |  
#       | DOOM     |  
