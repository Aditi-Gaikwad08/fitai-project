"""
diet.py — AI Dietician (Rule-Based)
=====================================
Calculates BMI and returns a structured diet plan
based on BMI category and the user's fitness goal.
No external API needed — fully rule-based logic.
"""


# ──────────────────────────────────────────────
# BMI CALCULATION
# ──────────────────────────────────────────────
def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """
    BMI = weight(kg) / height(m)²

    Returns BMI rounded to 1 decimal place.
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)


def get_bmi_category(bmi: float) -> str:
    """Return WHO BMI category string."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal"
    elif bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"


# ──────────────────────────────────────────────
# DIET PLAN DATABASE (Rule-Based)
# ──────────────────────────────────────────────
DIET_PLANS = {
    # goal → bmi_category → plan dict
    "lose": {
        "Underweight": {
            "calories": "1800–2000 kcal/day",
            "protein":  "High (1.6 g/kg body weight)",
            "carbs":    "Moderate",
            "fats":     "Moderate (healthy fats)",
            "note":     "⚠️ You are underweight. Avoid aggressive calorie cuts. Focus on quality nutrition.",
            "meals": [
                "Breakfast: Oats with banana + 2 boiled eggs",
                "Lunch: Grilled chicken + brown rice + salad",
                "Snack: Greek yoghurt + nuts",
                "Dinner: Dal + roti + steamed vegetables",
            ],
            "avoid":  ["Junk food", "Sugary drinks", "Processed snacks"],
        },
        "Normal": {
            "calories": "1600–1800 kcal/day",
            "protein":  "High (1.5 g/kg)",
            "carbs":    "Low–Moderate (complex carbs only)",
            "fats":     "Low",
            "note":     "Slight calorie deficit. Prioritise whole foods.",
            "meals": [
                "Breakfast: Egg whites + whole wheat toast + fruit",
                "Lunch: Salad with grilled paneer/chicken",
                "Snack: Apple + peanut butter",
                "Dinner: Soup + grilled fish/tofu",
            ],
            "avoid":  ["White bread", "Sugary drinks", "Fried food"],
        },
        "Overweight": {
            "calories": "1400–1600 kcal/day",
            "protein":  "High (1.8 g/kg)",
            "carbs":    "Low (cut refined carbs)",
            "fats":     "Low",
            "note":     "Calorie deficit of ~500 kcal/day recommended.",
            "meals": [
                "Breakfast: Vegetable omelette (no yolk) + green tea",
                "Lunch: Grilled chicken breast + large salad",
                "Snack: Cucumber + hummus",
                "Dinner: Lentil soup + steamed broccoli",
            ],
            "avoid":  ["Sugar", "Alcohol", "Refined carbs", "Fast food"],
        },
        "Obese": {
            "calories": "1200–1400 kcal/day",
            "protein":  "Very High (2.0 g/kg)",
            "carbs":    "Very Low",
            "fats":     "Minimal",
            "note":     "⚠️ Consult a doctor before starting. Aggressive deficit needed.",
            "meals": [
                "Breakfast: Boiled eggs + black coffee",
                "Lunch: Grilled lean meat + non-starchy veggies",
                "Snack: Handful of almonds",
                "Dinner: Grilled fish + salad",
            ],
            "avoid":  ["All sugar", "Alcohol", "Processed food", "High-calorie snacks"],
        },
    },

    "gain": {
        "Underweight": {
            "calories": "2800–3200 kcal/day",
            "protein":  "Very High (2.0 g/kg)",
            "carbs":    "High (complex carbs)",
            "fats":     "High (healthy fats)",
            "note":     "Calorie surplus of ~500 kcal/day. Eat every 3–4 hours.",
            "meals": [
                "Breakfast: Banana smoothie + peanut butter toast + eggs",
                "Lunch: Rice + chicken curry + curd",
                "Snack: Dry fruits + milk",
                "Dinner: Paneer + roti + sabzi + curd",
                "Post-workout: Protein shake + banana",
            ],
            "avoid":  ["Skipping meals", "Empty calories"],
        },
        "Normal": {
            "calories": "2500–2800 kcal/day",
            "protein":  "High (1.8 g/kg)",
            "carbs":    "High",
            "fats":     "Moderate",
            "note":     "Lean bulk. Aim for muscle gain, not fat.",
            "meals": [
                "Breakfast: Oats + milk + nuts + 3 eggs",
                "Lunch: Brown rice + dal + chicken",
                "Snack: Protein shake + fruits",
                "Dinner: Roti + sabzi + curd",
            ],
            "avoid":  ["Junk food", "Late-night eating"],
        },
        "Overweight": {
            "calories": "2200–2400 kcal/day",
            "protein":  "High (1.8 g/kg)",
            "carbs":    "Moderate",
            "fats":     "Moderate",
            "note":     "Focus on lean muscle. Avoid excessive fat gain.",
            "meals": [
                "Breakfast: Egg omelette + brown bread",
                "Lunch: Dal + rice + salad",
                "Snack: Greek yoghurt + berries",
                "Dinner: Grilled chicken + vegetables",
            ],
            "avoid":  ["Saturated fats", "Sugar", "Processed food"],
        },
        "Obese": {
            "calories": "2000–2200 kcal/day",
            "protein":  "High (1.8 g/kg)",
            "carbs":    "Moderate",
            "fats":     "Low",
            "note":     "⚠️ Focus on recomposition (lose fat, gain muscle). Consult a doctor.",
            "meals": [
                "Breakfast: Boiled eggs + oats",
                "Lunch: Grilled chicken + salad + dal",
                "Snack: Nuts",
                "Dinner: Fish + vegetables",
            ],
            "avoid":  ["High-calorie junk", "Sugar", "Alcohol"],
        },
    },

    "maintain": {
        "Underweight": {
            "calories": "2200–2500 kcal/day",
            "protein":  "Moderate (1.4 g/kg)",
            "carbs":    "Moderate",
            "fats":     "Moderate",
            "note":     "Try to slowly increase calorie intake to reach a healthy weight.",
            "meals": [
                "Breakfast: Paratha + curd + fruit",
                "Lunch: Dal + rice + sabzi",
                "Snack: Nuts + milk",
                "Dinner: Roti + paneer curry",
            ],
            "avoid":  ["Skipping meals"],
        },
        "Normal": {
            "calories": "2000–2300 kcal/day",
            "protein":  "Moderate (1.2 g/kg)",
            "carbs":    "Moderate",
            "fats":     "Moderate",
            "note":     "You're at a healthy weight! Maintain with balanced nutrition.",
            "meals": [
                "Breakfast: Poha / upma + tea",
                "Lunch: Dal + roti + sabzi + curd",
                "Snack: Fruit + nuts",
                "Dinner: Rice + dal + salad",
            ],
            "avoid":  ["Overeating", "Excessive junk"],
        },
        "Overweight": {
            "calories": "1800–2000 kcal/day",
            "protein":  "Moderate–High (1.5 g/kg)",
            "carbs":    "Moderate",
            "fats":     "Low–Moderate",
            "note":     "Consider gentle weight loss for better health.",
            "meals": [
                "Breakfast: Idli + sambhar",
                "Lunch: Brown rice + dal + salad",
                "Snack: Buttermilk",
                "Dinner: Roti + sabzi",
            ],
            "avoid":  ["Fried snacks", "Sugary drinks"],
        },
        "Obese": {
            "calories": "1600–1800 kcal/day",
            "protein":  "High (1.8 g/kg)",
            "carbs":    "Low",
            "fats":     "Low",
            "note":     "⚠️ Maintaining at this weight increases health risks. Consult a doctor.",
            "meals": [
                "Breakfast: Sprouts + black coffee",
                "Lunch: Dal + salad",
                "Snack: Cucumber",
                "Dinner: Grilled chicken + soup",
            ],
            "avoid":  ["Sugar", "Alcohol", "Processed food"],
        },
    },
}


# ──────────────────────────────────────────────
# PUBLIC API
# ──────────────────────────────────────────────
def get_diet_plan(bmi: float, goal: str) -> dict:
    """
    Return a full diet plan dict for the given BMI and goal.

    Parameters:
        bmi  : float — calculated BMI
        goal : str   — 'lose' | 'gain' | 'maintain'

    Returns:
        dict with keys: category, calories, protein, carbs, fats,
                        note, meals, avoid
    """
    category = get_bmi_category(bmi)
    plan = DIET_PLANS.get(goal, DIET_PLANS["maintain"]).get(category, {})
    plan["category"] = category
    return plan
