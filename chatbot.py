"""
chatbot.py — Virtual Gym Buddy (v2 - Enhanced)
===============================================
Keyword-based chatbot with broader coverage and smarter matching.
get_response() is the only public function used by app.py.
"""

import random
import re

# ── Response database ────────────────────────────────────────────────────────
# Each key is a tuple of trigger substrings (matched via 'in' on lowercased input)
# Each value is a list of replies; one is chosen at random.

RESPONSES = {
    ("lazy", "don't feel like", "dont feel", "not motivated", "no motivation",
     "can't be bothered", "cant be bothered", "unmotivated", "procrastinat"):
        [
            "Every champion started by doing something when they didn't feel like it. Get up and do ONE set — momentum will carry you!",
            "Your future self is watching you right now. Show them what you're made of!",
            "Lazy days are normal. But goals don't take days off. Even 10 minutes today counts.",
            "The hardest part is tying your shoes. Put them on — your body will follow.",
            "Nobody ever regretted a workout. Everybody has regretted skipping one.",
        ],

    ("tired", "exhausted", "no energy", "fatigue", "fatigued", "drained",
     "burnout", "burnt out", "burned out"):
        [
            "Rest is part of training! If you're genuinely wiped out, take a recovery day — that's not quitting, it's smart.",
            "Try a light session: 20-min walk or stretching. Movement without intensity still helps.",
            "Dehydration causes 80% of gym fatigue. Drink a big glass of water, wait 10 minutes, then reassess.",
            "A 5-minute warm-up often banishes tiredness completely. Just start — your body will surprise you.",
        ],

    ("don't want", "dont want", "skip", "not today", "avoid", "cancel"):
        [
            "Skipping is a habit too — and it compounds just like working out does. Break it now.",
            "Make a deal with yourself: do just 5 minutes. If you still want to stop after 5 mins, fine. You won't want to stop.",
            "Your gym session is booked with your future self. Don't stand them up!",
        ],

    ("diet", "eat", "food", "nutrition", "meal", "calories", "calorie",
     "protein", "carb", "fat", "hungry", "hunger"):
        [
            "80% of fitness is diet! Head to the Diet tab to get your personalised meal plan.",
            "Protein is your best friend for muscle growth. Aim for 1.5–2 g per kg of body weight per day.",
            "Meal prep on Sundays = healthy eating all week. Try cooking 4–5 portions at once.",
            "Never skip breakfast — it kickstarts your metabolism and reduces cravings all day.",
            "Tip: eat slowly and stop at 80% full. Your gut signals take 20 minutes to reach your brain.",
        ],

    ("weight", "fat", "bulk", "lean", "muscle", "body"):
        [
            "Track progress weekly, not daily — the scale lies short-term due to water and glycogen.",
            "Muscle is denser than fat. Trust the process even when the scale barely moves.",
            "Set a SMART goal: Specific, Measurable, Achievable, Relevant, Time-bound.",
            "Body recomposition (lose fat + gain muscle simultaneously) is real — just slower. Be patient.",
        ],

    ("pain", "hurt", "injur", "sore", "ache", "cramp"):
        [
            "Pain is a signal — stop training that area immediately and rest it.",
            "Post-workout soreness (DOMS) is normal. Sharp pain during exercise is NOT — stop immediately.",
            "Persistent pain? See a physiotherapist. Pushing through injuries makes them 10x worse.",
            "Ice for acute injuries (first 48h), heat for chronic stiffness. When in doubt, rest.",
        ],

    ("result", "no result", "not seeing", "not working", "plateau", "progress",
     "not changing", "same weight"):
        [
            "Results take 4 weeks to FEEL, 8 weeks to SEE, 12 weeks for others to NOTICE. Be patient!",
            "Take progress photos every 2 weeks — the mirror lies, but photos don't.",
            "Hit a plateau? Time for progressive overload — add 5% weight or 1 extra rep each week.",
            "Check your diet — most plateaus are caused by eating more than you think (hidden calories).",
        ],

    ("hello", "hi ", "hey", "sup", "yo", "good morning", "good evening", "howdy", "what's up", "whats up"):
        [
            "Hey there, champion! Ready to crush today's workout?",
            "Hey! What can I help with — motivation, diet tips, or workout advice?",
            "Hello, warrior! How can your Gym Buddy help today?",
        ],

    ("thanks", "thank you", "thx", "ty ", "great job", "awesome", "perfect", "excellent"):
        [
            "You're welcome! Now go smash that session!",
            "Anytime! Remember — consistency beats intensity every single time.",
            "Keep grinding! You've absolutely got this.",
        ],

    ("bye", "goodbye", "see you", "later", "quit", "exit"):
        [
            "See you next session! Stay consistent — that's the secret.",
            "Goodbye, champion! Rest well and come back stronger.",
            "Later! Don't forget to log your workout in the Habit Tracker!",
        ],

    ("workout", "exercise", "gym", "train", "session", "lift", "lifting"):
        [
            "Great mindset! Launch pose_detector.py to start tracking your reps in real time.",
            "Today's mantra: one more rep. Always one more rep.",
            "Warm up for 5 minutes first — it reduces injury risk by 50% and improves performance.",
            "Beginner plan: 3 sets × 12 reps of bicep curls, squats, push-ups, and rows.",
        ],

    ("how many", "how much", "sets", "reps", "repetition"):
        [
            "Beginners: 3 sets × 10–12 reps. Intermediate: 4 sets × 8–10 reps.",
            "For strength: 5×5. For muscle size: 3–4×8–12. For endurance: 2–3×15–20.",
            "Rest 60 sec between sets for endurance, 90–120 sec for muscle, 2–3 min for max strength.",
        ],

    ("sleep", "rest", "recovery", "recover"):
        [
            "Sleep is when your muscles actually GROW. Aim for 7–9 hours minimum.",
            "Recovery days are not lazy days — they are muscle-building days.",
            "Poor sleep raises cortisol (fat-storage hormone) and kills gains. Protect your sleep.",
        ],

    ("water", "hydrat", "drink"):
        [
            "Drink at least 2–3 litres of water a day. More on training days.",
            "Even mild dehydration (2% body weight) tanks your workout performance significantly.",
            "A good rule: drink 500 ml 30 minutes before training and sip throughout.",
        ],

    ("motivat", "inspire", "quote", "encourage"):
        [
            "\"The body achieves what the mind believes.\" Keep believing!",
            "\"It never gets easier, you just get stronger.\" — Greg Plitt",
            "Small daily improvements lead to staggering long-term results. Stay the course.",
            "You are one workout away from a better mood. Go do it.",
        ],
}

# Fallback replies when nothing matches
FALLBACKS = [
    "I'm still learning! Try asking about workouts, diet, motivation, or recovery.",
    "Hmm, not sure about that one. Ask me: 'I feel lazy', 'diet tips', 'I'm tired', or 'how many reps?'",
    "Great question! Check the Diet or Habit tabs for specific tools, or ask me something fitness-related.",
    "I didn't quite catch that. Try: 'help with diet', 'not seeing results', or 'I want to skip today'.",
]


# ── Public API ───────────────────────────────────────────────────────────────

def get_response(user_input: str) -> str:
    """
    Match user_input against keyword groups and return a motivational reply.
    Matching is case-insensitive substring search.
    """
    text = user_input.lower().strip()

    # Remove punctuation for cleaner matching
    text_clean = re.sub(r"[^\w\s]", " ", text)

    for keywords, replies in RESPONSES.items():
        if any(kw in text_clean or kw in text for kw in keywords):
            return random.choice(replies)

    return random.choice(FALLBACKS)