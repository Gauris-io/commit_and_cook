import os
import requests
import google.generativeai as genai
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return "Backend is running! Use /api/data to fetch recipes."

# --- Configuration ---
AUTH_TOKEN = os.getenv("FLAVOR_DB_AUTH")
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') 

FLAVOR_DB_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AUTH_TOKEN}",
}

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview') # Using stable Gemini 3 alias

DISEASE_DATA = {
    "Diabetes": {"min": 11, "max": 13}, "Hypertension": {"min": 14, "max": 16},
    "Obesity": {"min": 8, "max": 10}, "Celiac": {"min": 12, "max": 14},
    "PCOS": {"min": 10, "max": 12}, "Heart Disease": {"min": 15, "max": 17},
    "Anemia": {"min": 9, "max": 11}, "GERD (Reflux)": {"min": 7, "max": 9}
}

@app.route('/api/data', methods=['GET'])
def get_integrated_data():
    disease = request.args.get('disease', 'Diabetes')
    region = request.args.get('region', 'Indian Subcontinent')
    diet = request.args.get('diet', 'vegan')
    
    config = DISEASE_DATA.get(disease, DISEASE_DATA["Diabetes"])
    
    mol_url = f"http://cosylab.iiitd.edu.in:6969/flavordb/molecules_data/filter-by-hbd-count-range?min={config['min']}&max={config['max']}&page=0&size=20"
    rec_url = f"http://cosylab.iiitd.edu.in:6969/recipe2-api/recipe/region-diet/region-diet?region={region}&diet={diet}&limit=5"

    try:
        # 1. Fetch Molecules
        mol_resp = requests.get(mol_url, headers=FLAVOR_DB_HEADERS)
        mol_json = mol_resp.json().get('content', [])
        cleaned_mols = [
            {
                "id": m.get('_id'),
                "name": m.get('common_name'),
                "flavor": (m.get('fooddb_flavor_profile') or "None").replace('@', ', '),
                "superSweet": m.get('supersweetdb_id')
            } for m in mol_json if m.get('supersweetdb_id')
        ]

        # 2. Fetch Recipes & Generate Instructions
        rec_resp = requests.get(rec_url, headers=FLAVOR_DB_HEADERS)
        raw_recipes = rec_resp.json().get('data', [])
        ai_recipes = []

        for rec in raw_recipes:
            title = rec.get('Recipe_title')
            prompt = f"Provide a brief {diet} recipe for '{title}' safe for {disease}. List ingredients and 3 steps."
            
            try:
                response = model.generate_content(prompt)
                content = response.text if response.text else "AI response error."
            except Exception as e:
                content = f"Recipe currently unavailable. (Error: {str(e)})"

            ai_recipes.append({"title": title, "instructions": content})

        return jsonify({"molecules": cleaned_mols, "recipes": ai_recipes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)