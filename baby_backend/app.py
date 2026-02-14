from flask import Flask, request, jsonify
from flask_cors import CORS
from service import process_recipe_request

app = Flask(__name__)
CORS(app)  # allows React (port 3000) to talk to Flask (port 5000)

@app.route("/get-recipes", methods=["POST"])
def get_recipes():
    try:
        print("ROUTE HIT")
        data = request.json
        print("DATA RECEIVED:", data)
        service_result = process_recipe_request(data)
        return jsonify({
            "message": "backend working",
            "service_output": service_result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
