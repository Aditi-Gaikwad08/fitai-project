# ⚡ FitAI — AI Gym & Fitness Assistant

A complete AI-powered fitness assistant built using **Python, Flask, MediaPipe, OpenCV, HTML/CSS/JS** with a modern UI and deployed web application.

---

## 🌐 Live Website

👉 https://fitai-project-xxxx.onrender.com  

> ⚠️ Note: The AI Gym Trainer (webcam) runs locally and is not available on the deployed website.

---

## 📁 Project Structure

```
FitAI_Project/
│
├── app.py # Flask backend (main server)
├── chatbot.py # AI Gym Buddy logic
├── diet.py # BMI + diet planner
├── habit_tracker.py # Habit tracking system
├── pose_detector.py # AI Gym Trainer (MediaPipe + OpenCV)
├── habit_data.json # Data storage
│
├── templates/ # HTML pages
│ ├── base.html
│ ├── index.html
│ ├── diet.html
│ ├── habit.html
│ └── chat.html
│
├── static/ # Frontend assets
│ ├── style.css
│ ├── main.js
│ └── chat.js
│
├── requirements.txt
├── render.yaml
├── runtime.txt
└── README.md
```


---

## 🧠 Key Features

### 🏠 Dashboard
- Clean, responsive UI
- Central navigation for all modules

### 🥗 Diet Planner
- BMI calculation (WHO formula)
- Goal-based diet recommendations

### 📊 Habit Tracker
- Daily workout logging
- Streak calculation
- 14-day consistency tracking
- Lightweight JSON storage

### 💬 AI Gym Buddy
- Interactive chatbot
- Motivation + diet + workout advice
- Real-time API-based responses

### 🎯 AI Gym Trainer (Computer Vision)
- Real-time **Bicep Curl Counter**
- Dual-arm tracking
- Angle-based rep detection
- Performance scoring (0–100)
- Built using MediaPipe Pose Estimation

---

## 🧱 Tech Stack

| Layer       | Technology |
|------------|-----------|
| Backend    | Flask (Python) |
| Frontend   | HTML, CSS, JavaScript |
| AI / CV    | MediaPipe, OpenCV |
| Data       | JSON |
| Deployment | Render |

---

## ⚙️ System Architecture

- **Frontend:** UI + API calls  
- **Backend (Flask):** Business logic + routing  
- **Computer Vision Module:** Runs locally using OpenCV + MediaPipe  
- **Data Layer:** JSON-based persistence  

---

## 🚀 Running the Project

### 🌐 Web Application (Deployed)

Access the live project here:

👉 https://fitai-project-nr11.onrender.com

This includes:
- Dashboard
- Diet Planner
- Habit Tracker
- Chatbot

No installation required.

---

### 💻 AI Gym Trainer (Local Module)

The pose detection module runs locally:

```bash
python pose_detector.py
⚠️ Webcam Limitation (Design Decision)

The AI Trainer uses:

cv2.VideoCapture(0)

This requires direct access to the system webcam.

Environment	Supported
Local Machine	✅ Yes
Cloud (Render/Vercel)	❌ No
🧠 Design Approach

FitAI follows a hybrid architecture:

🌐 Cloud Layer → Web interface (Render)
💻 Edge Layer → Real-time pose detection (local)

This ensures:

Real-time performance
No video latency
Efficient processing
🧠 How It Works
Pose Detection
MediaPipe detects 33 body landmarks
Uses shoulder, elbow, wrist joints
Rep Counting Logic
Arm extended (>160°) → Down
Arm curled (<40°) → Up
Rep counted on Up → Down transition
Performance Score
Measures movement quality
Scaled between 0–100
💬 Chatbot Capabilities

Example inputs:

"I feel lazy"
"Diet tips"
"Not seeing results"
"How many sets?"
📈 Future Enhancements
Browser-based webcam integration (WebRTC)
Multi-exercise detection
User authentication system
Cloud database integration
Advanced analytics dashboard
🎓 Key Learnings
Real-time pose estimation using computer vision
Flask-based API development
Full-stack integration
Handling deployment constraints for AI systems
👩‍💻 Author

Aditi Gaikwad

⭐ Conclusion

FitAI demonstrates the integration of AI, web technologies, and real-time analytics to build an interactive fitness assistant. It highlights both technical implementation and practical deployment considerations in modern AI systems.