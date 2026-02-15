import requests
from google import genai
import json
import os


def validate_texture_for_age(age, textures):

    if age < 6:
        return {"error": "Solid food not recommended under 6 months"}

    if age <= 8:
        allowed = {"Puree", "Blend", "Mash"}
    elif age <= 10:
        allowed = {"Puree", "Blend", "Mash", "Boil", "Steam", "Crockpot","Bake","Blanch","Dice","Cook","Braize"}
    else:
        return None

    for texture in textures:
        if texture not in allowed:
            return {"error": f"{texture} not safe for this age"}

    return None
def score_recipe(recipe, textures, age):

    processes = recipe.get("Processes", "").lower()
    title = recipe.get("Recipe_title", "").lower()

    score = 0

    # -----------------------
    #  Texture Match (High weight)
    # -----------------------
    for t in textures:
        if t.lower() in processes:
            score += 8   # strong reward

    
    #  Soft Cooking Bonus
    soft_methods = ["steam", "boil", "crockpot", "braize", "blend", "puree", "mash"]
    for method in soft_methods:
        if method in processes:
            score += 3

    
    #  Penalize Harsh Cooking
    harsh_methods = ["fry", "deep fry", "grill", "barbecue"]
    for method in harsh_methods:
        if method in processes:
            score -= 6


     # Spice Penalty (important for babies)
    spicy_words = ["chili", "spicy", "hot", "pepper", "masala"]
    for word in spicy_words:
        if word in title or word in processes:
            score -= 7

    
    #  Process Simplicity
    process_steps = processes.split("||")
    if len(process_steps) <= 6:
        score += 4   # simpler is better
    elif len(process_steps) > 12:
        score -= 3

    
    #  Age-based softness adjustment
    
    if age <= 8:
        if any(x in processes for x in ["puree", "blend", "mash"]):
            score += 5
        else:
            score -= 4

    
    #  Dessert / Sweet Natural Bonus
    
    sweet_words = ["banana", "apple", "sweet potato", "pumpkin"]
    for word in sweet_words:
        if word in title:
            score += 2

    return score
def generate_baby_recipe(formatted_recipe, age, textures, allergies):
        print("KEY VALUE:", os.getenv("GEMINI_API_KEY"))
        print(" Gemini function started")
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        prompt = f"""
            You are a pediatric nutrition expert.

            Modify the following recipe to make it safe and appropriate for a {age}-month-old baby.

            Important Rules:
            - Follow WHO infant feeding guidelines.
            - No added salt.
            - No added sugar.
            - No honey.
            -Avoid foods high in trans fats
            -Avoid foods that pose choking risk (e.g., whole nuts, hard pieces, whole grapes)
            -No sweetened or flavoured milk products
            -Avoid unsafe preparation (undercooked meat)
            -No egg before 1 year
            -WHO strongly encourages:
             Daily animal-source foods (meat, poultry, fish, eggs) when available
             Especially iron-rich foods starting at 6 months
            - No spicy ingredients.
            - Avoid allergens: {allergies}
            -Adjust texture to match: {textures}
            - If texture does not match, modify instructions to achieve that texture.
            - Keep ingredients natural and simple.
            - Provide exact baby portion measurements.
            - Make steps extremely clear and simple.
            If recipe texture does not match, modify cooking method accordingly.
            If ingredients are too spicy, replace with mild baby-safe alternatives.
            Keep nutrition balanced and slightly umami or naturally sweet.
           NOTE - DO NOT CHNAGE THE RECIPE, JUST MODIFY IT WITH RESPECT TO GUIDANCE
           Return output strictly in JSON format like this:

          {{
             "title": "",
             "age_group": "{age} months",
             "texture_level": "",
             "ingredients": [
          {{"ingredient": "", "quantity": ""}}
         ],
            "instructions": [
                  "Step 1 ...",
                  "Step 2 ..."
             ],
           "nutrition_notes": "",
           "safety_notes": ""
      }}

       Here is the original recipe:

      {json.dumps(formatted_recipe, indent=2)}
      """
        llm_response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
      ) 
        print(llm_response.text)
        print("Gemini responded")
        return llm_response.text


def process_recipe_request(data):
    age = int(data.get("age", 0))
    texture = data.get("texture")
    cuisine = data.get("cuisine")
    diet = data.get("diet")  
    allergies = data.get("allergies", [])
    if age <= 0:
     return {"error": "Invalid age"}
    validation_error = validate_texture_for_age(age, texture)
    if validation_error:
        return validation_error
    print("Processing in services layer...")
    print(data)
    
    url = "https://api.foodoscope.com/recipe2-api/recipe/region-diet/region-diet"
    params = {
       'region': cuisine,
       'diet': diet,
       'limit': 10
   }
    headers = {
       "Content-Type": "application/json",
       "Authorization": "Bearer OYlwwj2JNPwD-RniWQYjz1U7vyYtneHkOVQJIR1qWhUjftg1",
   }
    response = requests.get(
    url,
    params=params,
    headers=headers
   )
    
    response_json = response.json()
    recipes = response_json.get("data", [])

    recipe_ids = set(recipe["_id"] for recipe in recipes)
    print("Recipe IDs:", recipe_ids)
    textures = data.get("texture", [])

    filtered_recipes = [
    recipe for recipe in recipes
    if any(t.lower() in recipe.get("Processes", "").lower() for t in textures)
  ] 
    pagination = response_json.get("pagination", {})
    current_page = pagination.get("currentPage")
    print("Current Page:", current_page)
    print("Filtered Recipes:", filtered_recipes)

    if filtered_recipes:
     print("Using filtered recipes")
     candidate_recipes = filtered_recipes
    else:
     print("No texture match found — using all region recipes")
     candidate_recipes = recipes

    
    if not candidate_recipes:
     return []

    scored_recipes = []

    for recipe in candidate_recipes:
     recipe_score = score_recipe(recipe, textures, age)
     scored_recipes.append((recipe_score, recipe))

    scored_recipes.sort(key=lambda x: x[0], reverse=True)

    best_score, best_recipe = scored_recipes[0]

    formatted_recipe = {
     "id": best_recipe.get("_id"),
     "title": best_recipe.get("Recipe_title"),
     "region": best_recipe.get("Region"),
     "continent": best_recipe.get("Continent"),
     "processes": best_recipe.get("Processes"),
     "nutrition": {
        "calories": best_recipe.get("Calories"),
        "protein": best_recipe.get("Protein (g)"),
        "fat": best_recipe.get("Total lipid (fat) (g)")
      },
     "time": {
        "prep": best_recipe.get("prep_time"),
        "cook": best_recipe.get("cook_time"),
        "total": best_recipe.get("total_time")
     },
     "servings": best_recipe.get("servings")
   }
    print("Formatted Recipe:", formatted_recipe)
      
    baby_recipe = generate_baby_recipe(
    formatted_recipe,
    age,
    textures,
    allergies
  )
    try:
     cleaned_text = baby_recipe.replace("```json", "").replace("```", "").strip()
     baby_recipe_json = json.loads(cleaned_text)
    except Exception:
     baby_recipe_json = {
        "error": True,
        "raw_response": baby_recipe
    }
     return {
    "original_recipe": formatted_recipe,
    "baby_friendly_recipe": baby_recipe_json
   }
   

    

    