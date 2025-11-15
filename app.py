from flask import Flask, render_template, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# Mock food data
foods = [
    {"name": "Milk", "expiry": "2025-11-10"},
    {"name": "Apple", "expiry": "2025-11-15"},
    {"name": "Bread", "expiry": "2025-11-08"},
    {"name": "Carrots", "expiry": "2025-11-20"}
]

nutrition_data = {
    "roti": {"protein": 3, "carbs": 15, "fat": 1},
    "dal": {"protein": 9, "carbs": 20, "fat": 1},
    "apple": {"protein": 0, "carbs": 14, "fat": 0},
    "milk": {"protein": 8, "carbs": 12, "fat": 4},
    "rice": {"protein": 2, "carbs": 28, "fat": 0},
    "banana": {"protein": 1, "carbs": 23, "fat": 0}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    today = datetime.now().date()
    fresh_foods = []
    expired_foods = []

    for f in foods:
        expiry_date = datetime.strptime(f["expiry"], "%Y-%m-%d").date()
        days_left = (expiry_date - today).days
        if days_left >= 0:
            fresh_foods.append({"name": f["name"], "days_left": days_left})
        else:
            expired_foods.append({"name": f["name"], "days_left": days_left})

    return render_template('dashboard.html', fresh=fresh_foods, expired=expired_foods)

@app.route('/add_food', methods=['POST'])
def add_food():
    data = request.json
    name = data.get("name")
    expiry = data.get("expiry")

    if name and expiry:
        foods.append({"name": name, "expiry": expiry})
        return jsonify({"message": "Food added successfully!"}), 200
    return jsonify({"message": "Invalid input!"}), 400

@app.route('/suggestions', methods=['POST'])
def suggestions():
    food_name = request.json.get('food')
    suggestions = {
        "Milk": ["Make paneer", "Use in compost for garden", "Make milk-based face mask"],
        "Bread": ["Make breadcrumbs", "Feed birds", "Compost it naturally"],
        "Apple": ["Make smoothie", "Bake apple pie", "Compost peels"],
        "Carrots": ["Make carrot halwa", "Use peels in compost", "Make carrot juice"]
    }
    return jsonify({"ideas": suggestions.get(food_name, ["No suggestions found!"])})

@app.route('/nutrition')
def nutrition_page():
    return render_template('nutrition.html')

@app.route('/analyze_nutrition', methods=['POST'])
def analyze_nutrition():
    foods_list = request.json.get('foods', [])
    totals = {"protein": 0, "carbs": 0, "fat": 0}

    for food in foods_list:
        data = nutrition_data.get(food.lower())
        if data:
            for key in totals:
                totals[key] += data[key]

    advice = []
    if totals["protein"] < 20:
        advice.append("Add more protein — try lentils, paneer, or tofu.")
    if totals["carbs"] < 50:
        advice.append("You need more energy — include rice or fruits.")
    if totals["fat"] < 10:
        advice.append("Healthy fats missing — add nuts or olive oil.")
    if not advice:
        advice.append("Perfect balance! Keep it up 👍")

    return jsonify({"totals": totals, "advice": advice})

if __name__ == '__main__':
    app.run(debug=True)
