import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
# Sabse zaroori step: Iske bina data block ho jata hai
CORS(app)

# Env variables se keys load ho rahi hain
AUTH_TOKEN = os.getenv("FLAVOR_DB_AUTH")
HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}"}

DISEASE_DATA = {
    "Diabetes": {"min": 11, "max": 13, "diet": "low-glycemic", "nutrients": {"Fiber": "High", "Sugar": "Low"}},
    "Hypertension": {"min": 14, "max": 16, "diet": "low-sodium", "nutrients": {"Potassium": "High", "Sodium": "Low"}},
    "Obesity": {"min": 8, "max": 10, "diet": "low-fat", "nutrients": {"Calories": "Low", "Protein": "High"}},
    "Celiac": {"min": 12, "max": 14, "diet": "gluten-free", "nutrients": {"Gluten": "Zero", "Iron": "High"}},
    "PCOS": {"min": 10, "max": 12, "diet": "high-protein", "nutrients": {"Fiber": "High", "Glycemic": "Low"}},
    "Heart Disease": {"min": 15, "max": 17, "diet": "low-cholesterol", "nutrients": {"Omega-3": "High", "Trans-fats": "Zero"}},
    "Anemia": {"min": 9, "max": 11, "diet": "high-iron", "nutrients": {"Iron": "Very High", "Vit C": "High"}},
    "GERD (Reflux)": {"min": 7, "max": 9, "diet": "alkaline", "nutrients": {"Acidity": "Low", "Spices": "Mild"}}
}

@app.route('/api/research', methods=['GET'])
def get_research_data():
    disease_name = request.args.get('disease', 'Diabetes')
    config = DISEASE_DATA.get(disease_name, DISEASE_DATA["Diabetes"])
    try:
        # Fetch Molecules from FlavorDB
        mol_url = "http://cosylab.iiitd.edu.in:6969/flavordb/molecules_data/by-heavyAtomCount-range"
        mol_params = {'min': config['min'], 'max': config['max'], 'size': 15}
        mol_resp = requests.get(mol_url, params=mol_params, headers=HEADERS, timeout=10).json()
        
        molecules = [{"name": i.get('common_name', 'Unknown'), "flavor": i.get('fooddb_flavor_profile', '').replace('@', ', ')} for i in mol_resp.get('content', [])]

        # Fetch Recipes from Recipe2-API
        rec_url = "http://cosylab.iiitd.edu.in:6969/recipe2-api/recipe/region-diet/region-diet"
        rec_params = {'region': 'Indian Subcontinent', 'diet': config['diet'], 'limit': 6}
        rec_resp = requests.get(rec_url, params=rec_params, headers=HEADERS, timeout=10).json()

        return jsonify({"success": True, "molecules": molecules, "recipes": rec_resp.get('data', []), "nutrients": config['nutrients']})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)