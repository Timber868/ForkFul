from behave import given, when, then
import json

@given("a recipe post exists")
def step_recipe_post_exists(context):
    context.recipe_name = "Test Recipe Reactions"

    response = context.client.get(f'/recipes/')
    assert response.status_code == 200, "Failed to fetch recipe posts."
    
    context.recipes = json.loads(response.data)
    
    recipe_exists = any(recipe["name"] == context.recipe_name for recipe in context.recipes)
    assert recipe_exists, f"Recipe with name {context.recipe_name} does not exist."
    
    context.recipe_id = next(recipe["id"] for recipe in context.recipes if recipe["name"] == context.recipe_name)

    response = context.client.get(f'/reactions?user_id={context.user_id}&recipe_id={context.recipe_id}')
    assert response.status_code == 200, "Failed to fetch reactions."
    context.reactions = json.loads(response.data)
    context.original_reactions = context.reactions.copy()

@given("I have not reacted to the post before")
def step_no_reaction_before(context):
    response = context.client.delete(f'/reactions', json={
        "user_id": context.user_id,
        "recipe_id": context.recipe_id,
    })
    assert response.status_code == 200, "Failed to clear previous reaction."
    
    response = context.client.get(f'/reactions?user_id={context.user_id}&recipe_id={context.recipe_id}')
    assert response.status_code == 200, "Failed to fetch reactions."

    context.original_reactions = json.loads(response.data)
    assert context.original_reactions["user_reaction"] is None, f"User has already reacted to the post."

@given('I have already reacted to the post with "{reaction}"')
def step_already_reacted(context, reaction):
    reaction = 1 if reaction == "BOOM" else 0
    response = context.client.post(f'/reactions', json={
        "user_id": context.user_id,
        "recipe_id": context.recipe_id,
        "reaction": reaction
    })
    assert response.status_code == 201, "Failed to add reaction."

    response = context.client.get(f'/reactions?user_id={context.user_id}&recipe_id={context.recipe_id}')
    assert response.status_code == 200, "Failed to fetch reactions."
    
    context.original_reactions = json.loads(response.data)
    assert context.original_reactions["user_reaction"] == reaction, f"User reaction is not {context.reaction}"

@given("multiple users have reacted to the post")
def step_multiple_users_reacted(context):
    assert "booms" in context.original_reactions, "BOOM count not present in response"
    assert "dooms" in context.original_reactions, "DOOM count not present in response"
    assert (context.original_reactions["booms"] + context.original_reactions["dooms"]) > 1, "Total reactions should be greater than 1"
    
@when('I react to the post with "{reaction}"')
def step_react_to_post(context, reaction):
    reaction = 1 if reaction == "BOOM" else 0
    response = context.client.post(f'/reactions', json={
        "user_id": context.user_id,
        "recipe_id": context.recipe_id,
        "reaction": reaction
    })
    assert response.status_code == 201, "Failed to add reaction."

    response = context.client.get(f'/reactions?user_id={context.user_id}&recipe_id={context.recipe_id}')
    assert response.status_code == 200, "Failed to fetch reactions."
    context.reactions = json.loads(response.data)

@when('I change my reaction to "{reaction}"')
def step_change_reaction(context, reaction):
    step_react_to_post(context, reaction)

@when("I remove my reaction")
def step_remove_reaction(context):
    response = context.client.delete('/reactions', json={
        "user_id": context.user_id,
        "recipe_id": context.recipe_id,
    })
    assert response.status_code == 200, "Failed to remove reaction."

    response = context.client.get(f'/reactions?user_id={context.user_id}&recipe_id={context.recipe_id}')
    assert response.status_code == 200, "Failed to fetch reactions."
    context.reactions = json.loads(response.data)

@when("I view the post")
def step_view_post(context):
    response = context.client.get(f'/recipes/')
    assert response.status_code == 200, "Failed to fetch recipe posts."
    
    context.recipes = json.loads(response.data)
    recipe_exists = any(recipe["id"] == context.recipe_id for recipe in context.recipes)
    assert recipe_exists, f"Recipe with ID {context.recipe_id} does not exist."

@then('the reaction "{reaction}" should be recorded for the post')
def step_reaction_recorded(context, reaction):
    reaction = 1 if reaction == "BOOM" else 0

    response = context.client.get(f'/reactions?user_id={context.user_id}&recipe_id={context.recipe_id}')
    assert response.status_code == 200, "Failed to fetch reactions."
    context.reactions = json.loads(response.data)

    assert context.reactions["user_reaction"] is not None, "User reaction is not recorded"
    assert context.reactions["user_reaction"] == reaction, f"User reaction is not {reaction}"

@then("the total reaction count should be updated")
def step_total_reaction_count_updated(context):
    assert "booms" in context.reactions, "BOOM count not present in response"
    assert "dooms" in context.reactions, "DOOM count not present in response"
    assert (context.reactions["booms"] != context.original_reactions["booms"]) or (context.reactions["dooms"] != context.original_reactions["dooms"]), "Total reaction count should be updated"

@then('my reaction should be updated to "{reaction}"')
def step_reaction_updated(context, reaction):
    reaction = 1 if reaction == "BOOM" else 0
    assert context.reactions["user_reaction"] == reaction, f"User reaction is not {reaction}"

@then("the reaction count should reflect the change")
def step_reaction_count_reflect_change(context):
    assert "booms" in context.reactions, "BOOM count not present in response"
    assert "dooms" in context.reactions, "DOOM count not present in response"

    if context.reactions["user_reaction"] == 1:
        assert context.reactions["booms"] > context.original_reactions["booms"], "BOOM count should have increased"
        assert context.reactions["dooms"] < context.original_reactions["dooms"], "DOOM count should remain unchanged"
    else:
        assert context.reactions["dooms"] > context.original_reactions["dooms"], "DOOM count should have increased"
        assert context.reactions["booms"] < context.original_reactions["booms"], "BOOM count should remain unchanged"

@then("the reaction should be removed from the post")
def step_reaction_removed(context):
    assert context.reactions["user_reaction"] is None, "User reaction is still recorded"

@then("I should see the total number of BOOM and DOOM reactions")
def step_view_total_reactions(context):
    assert "booms" in context.reactions, "BOOM count not present in response"
    assert "dooms" in context.reactions, "DOOM count not present in response"