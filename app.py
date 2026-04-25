"""
AI Gym & Fitness Assistant — Flask Application (v2)
"""

from flask import Flask, render_template, request, jsonify
from diet import calculate_bmi, get_diet_plan
from habit_tracker import log_workout, get_streak, get_history, get_consistency
from chatbot import get_response
import os

app = Flask(__name__)


# ── PAGES ────────────────────────────────────────

@app.route("/")
def index():
    streak = get_streak()
    consistency = get_consistency()
    return render_template("index.html", streak=streak, consistency=consistency)


@app.route("/diet", methods=["GET", "POST"])
def diet():
    result = None
    if request.method == "POST":
        try:
            weight = float(request.form["weight"])
            height = float(request.form["height"])
            goal   = request.form["goal"]
            bmi    = calculate_bmi(weight, height)
            plan   = get_diet_plan(bmi, goal)
            result = {"bmi": bmi, "plan": plan, "goal": goal}
        except (ValueError, KeyError) as e:
            result = {"error": str(e)}
    return render_template("diet.html", result=result)


@app.route("/habit", methods=["GET", "POST"])
def habit():
    message = None
    if request.method == "POST":
        did_workout = request.form.get("workout") == "yes"
        log_workout(did_workout)
        message = "Workout logged successfully!" if did_workout else "Rest day logged."

    streak      = get_streak()
    history     = get_history()
    consistency = get_consistency()

    return render_template(
        "habit.html",
        streak=streak,
        history=history,
        message=message,
        consistency=consistency
    )


@app.route("/chat")
def chat():
    return render_template("chat.html")


# ── API (ONLY ONE CHAT ROUTE) ─────────────────────

@app.route("/api/chat", methods=["POST"])
def api_chat():
    if not request.is_json:
        return jsonify({"reply": "Invalid request format.", "status": "error"}), 400

    data = request.get_json(silent=True) or {}
    user_msg = data.get("message", "").strip().lower()

    if not user_msg:
        return jsonify({"reply": "Please type something!", "status": "empty"})

    # simple fallback logic + chatbot
    if "lazy" in user_msg:
        reply = "Start small. Even 5 minutes of workout beats zero. Let’s go 💪"
    elif "tired" in user_msg:
        reply = "Rest is important, but light movement can boost energy ⚡"
    elif "diet" in user_msg:
        reply = "Focus on protein, hydration, and balanced meals 🥗"
    elif "not seeing results" in user_msg:
        reply = "Stay consistent. Results take time. Trust the process 🔥"
    else:
        reply = get_response(user_msg)

    return jsonify({"reply": reply, "status": "ok"})


# ── RUN (RENDER SAFE) ────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)