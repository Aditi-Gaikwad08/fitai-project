# ⚡ FitAI — AI Gym & Fitness Assistant

A complete AI-powered fitness assistant built with Python, Flask, MediaPipe, and OpenCV.

---

## 📂 Project Structure

```
fitness_assistant/
├── app.py              ← Flask web server (main entry point)
├── pose_detector.py    ← AI Gym Trainer (webcam + MediaPipe)
├── diet.py             ← BMI calculator + diet recommendation
├── habit_tracker.py    ← Workout habit tracker (JSON storage)
├── chatbot.py          ← Virtual Gym Buddy (keyword chatbot)
├── templates/
│   ├── base.html       ← Shared nav + layout
│   ├── index.html      ← Dashboard
│   ├── diet.html       ← Diet page
│   ├── habit.html      ← Habit tracker page
│   └── chat.html       ← Chatbot page
├── static/
│   ├── css/style.css   ← Dark athletic UI styles
│   └── js/
│       ├── main.js     ← Shared JS
│       └── chat.js     ← Chat UI logic
├── requirements.txt
└── README.md
```

---

## 🚀 Setup Instructions (Step-by-Step)

### Step 1 — Prerequisites

- Python **3.9 – 3.11** (MediaPipe does not yet support 3.12+)
- A working **webcam**
- Windows / macOS / Linux

### Step 2 — Create a Virtual Environment (Recommended)

```bash
# Navigate to project folder
cd fitness_assistant

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS / Linux)
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ If MediaPipe fails on Windows, try: `pip install mediapipe --pre`

### Step 4 — Run the Web App (Flask)

```bash
python app.py
```

Open your browser → **http://127.0.0.1:5000**

### Step 5 — Run the AI Gym Trainer (Webcam)

Open a **second terminal** in the same folder (with venv activated):

```bash
python pose_detector.py
```

A window will open showing your webcam feed with pose landmarks.

---

## 🏋️ How to Use the Bicep Curl Counter

1. **Stand** so your upper body is fully visible to the webcam.
2. **Position** your right arm at your side — elbow angle should be > 160° → screen shows `STAGE: down`.
3. **Curl** your forearm all the way up until elbow angle < 40° → screen shows `STAGE: up`.
4. **Lower** your arm back down past 160° → **REP counter increments by 1**. ✅
5. Repeat for more reps.
6. Press **Q** to quit and see your final score.

### Expected Angle Ranges

| Position        | Angle         |
|-----------------|---------------|
| Arm extended    | 160° – 180°   |
| Arm fully curled| 20° – 40°     |

---

## 🌐 Web App Features

| Page       | URL          | Description                                 |
|------------|--------------|---------------------------------------------|
| Dashboard  | `/`          | Overview + pose detector instructions       |
| Dietician  | `/diet`      | BMI calculator + personalised diet plan     |
| Habits     | `/habit`     | Log workouts, view streak & 14-day history  |
| Gym Buddy  | `/chat`      | AI chatbot with motivational responses      |

---

## 🐛 Common Errors & Fixes

### ❌ Counter stuck at 0

**Cause:** You're not completing a full range of motion.  
**Fix:** Fully extend your arm (> 160°) then fully curl (< 40°). The counter only increments when you go from "up" → "down".

### ❌ Stage not changing

**Cause:** Lighting too dark, arm not in frame, or wrong angle thresholds.  
**Fix:** Improve lighting. Ensure full arm is visible. In `pose_detector.py`, adjust:
```python
DOWN_ANGLE = 155   # lower this if stage won't switch to "down"
UP_ANGLE   = 50    # raise this if stage won't switch to "up"
```

### ❌ Flickering detection / jumpy angle

**Cause:** Low confidence or fast movement.  
**Fix:** Increase confidence thresholds in `pose_detector.py`:
```python
min_detection_confidence=0.7,
min_tracking_confidence=0.7
```

### ❌ `No module named mediapipe`

**Fix:** Ensure venv is activated and run `pip install mediapipe`.

### ❌ `Cannot read from webcam`

**Fix:** Check if another app is using the webcam. Try `cv2.VideoCapture(1)` instead of `0`.

### ❌ Flask `Address already in use`

**Fix:** Kill the process using port 5000, or change the port:
```python
app.run(debug=True, port=5001)
```

---

## 📊 Performance Score Explained

The live score (0–100) displayed in the pose detector window measures:

- **Up quality**: How fully you curl (closer to 0° = better, ideal ≤ 40°)
- **Down quality**: How fully you extend (closer to 180° = better, ideal ≥ 160°)

Score = average of up + down quality scores across all reps.

---

## 💬 Chatbot Keywords

Try saying these to the Gym Buddy:

| Input               | Category             |
|---------------------|----------------------|
| I feel lazy         | Motivation           |
| I'm tired           | Energy / rest        |
| Skip workout        | Accountability       |
| Diet tips           | Nutrition            |
| Not seeing results  | Progress             |
| I feel pain         | Injury warning       |
| How many sets?      | Training advice      |

---

## 🎓 Viva Explanation (Short)

**Q: What AI/ML is used?**  
A: MediaPipe's Pose Estimation model detects 33 body landmarks using a pre-trained deep learning model. We then apply geometry (3-point angle formula) to count exercise reps.

**Q: How does rep counting work?**  
A: We compute the elbow joint angle from 3 landmarks (shoulder, elbow, wrist). When the angle exceeds 160° the stage is "down"; when it goes below 40° the stage is "up". A complete rep is counted each time the stage transitions from "up" back to "down".

**Q: What is the performance score?**  
A: It measures how close each rep's peak angle is to the ideal range. A perfect curl (≤ 40° up, ≥ 160° down) scores 100.

**Q: How is diet calculated?**  
A: Using the WHO BMI formula (weight / height²), we classify the user into Underweight / Normal / Overweight / Obese and look up a pre-defined diet plan based on their goal (lose / gain / maintain).

**Q: How does the habit tracker work?**  
A: Each day's workout status is stored in a `habit_data.json` file. The streak is calculated by counting consecutive workout days backwards from today.

---

Built with ❤️ using Python · Flask · MediaPipe · OpenCV · HTML/CSS/JS
