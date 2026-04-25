"""
pose_detector.py — AI Gym Trainer v2 (Bicep Curl Counter — Both Arms)
=======================================================================
Improvements over v1:
  • Dual-arm detection (LEFT + RIGHT tracked independently)
  • Auto-switch: highlights the arm with more movement
  • Robust angle calculation — never returns NaN or crashes
  • Smoothed angle via rolling average (no flickering)
  • Corrected thresholds: DOWN > 150 deg, UP < 40 deg
  • Performance scorer per arm
  • Cleaner HUD overlay

HOW TO TEST:
  1. Run:  python pose_detector.py
  2. Stand so your FULL upper body is visible.
  3. Curl either arm — its reps are counted independently.
  4. Press Q to quit.

ANGLE RANGES:
  Arm extended (down): ~150°–180°
  Arm fully curled (up):  ~15°–40°

FIXES FOR COMMON BUGS:
  Counter at 0  → do a COMPLETE range of motion (fully extend, fully curl)
  Stage frozen  → adjust DOWN_ANGLE / UP_ANGLE constants below
  Flickering    → SMOOTH_WINDOW constant controls rolling average size
"""

import cv2
import mediapipe as mp
import numpy as np
from collections import deque

# ── Thresholds ───────────────────────────────────────────────────────────────
DOWN_ANGLE   = 150   # arm considered "down" (extended) when angle > this
UP_ANGLE     = 40    # arm considered "up" (curled) when angle < this
SMOOTH_WINDOW = 5    # frames for rolling-average smoothing

# ── MediaPipe setup ──────────────────────────────────────────────────────────
mp_drawing = mp.solutions.drawing_utils
mp_pose    = mp.solutions.pose

# ── Arm landmark indices ─────────────────────────────────────────────────────
ARMS = {
    "RIGHT": {
        "shoulder": mp_pose.PoseLandmark.RIGHT_SHOULDER,
        "elbow":    mp_pose.PoseLandmark.RIGHT_ELBOW,
        "wrist":    mp_pose.PoseLandmark.RIGHT_WRIST,
        "color":    (0, 255, 100),   # green
    },
    "LEFT": {
        "shoulder": mp_pose.PoseLandmark.LEFT_SHOULDER,
        "elbow":    mp_pose.PoseLandmark.LEFT_ELBOW,
        "wrist":    mp_pose.PoseLandmark.LEFT_WRIST,
        "color":    (100, 200, 255), # blue
    },
}


# ── Angle calculation ────────────────────────────────────────────────────────

def calculate_angle(a, b, c) -> float:
    """
    Compute the interior angle (degrees) at point B in the triangle A-B-C.
    Returns a float in [0, 180]. Never raises; returns 0.0 on bad input.

    Parameters
    ----------
    a, b, c : array-like [x, y]
    """
    try:
        a = np.array(a, dtype=float)
        b = np.array(b, dtype=float)
        c = np.array(c, dtype=float)

        ba = a - b
        bc = c - b

        # Guard against zero-length vectors
        norm_ba = np.linalg.norm(ba)
        norm_bc = np.linalg.norm(bc)
        if norm_ba == 0 or norm_bc == 0:
            return 0.0

        cos_angle = np.dot(ba, bc) / (norm_ba * norm_bc)
        # Clamp to [-1, 1] to avoid acos domain errors from floating-point drift
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        return float(np.degrees(np.arccos(cos_angle)))
    except Exception:
        return 0.0


# ── Arm tracker ──────────────────────────────────────────────────────────────

class ArmTracker:
    """Tracks stage, rep count, and angle history for one arm."""

    def __init__(self, name: str, color: tuple):
        self.name    = name
        self.color   = color
        self.counter = 0
        self.stage   = None          # "up" | "down" | None
        self.angle   = 0.0
        self._buf    = deque(maxlen=SMOOTH_WINDOW)  # angle smoothing buffer
        self._min_angle_rep = 180.0  # best curl angle this rep
        self._max_angle_rep = 0.0    # best extension angle this rep
        self.scores  = []            # per-rep quality scores

    def update(self, raw_angle: float):
        """Feed a new angle reading; update stage and counter."""
        # --- smoothing ---
        self._buf.append(raw_angle)
        self.angle = float(np.mean(self._buf))

        # --- range tracking ---
        self._min_angle_rep = min(self._min_angle_rep, self.angle)
        self._max_angle_rep = max(self._max_angle_rep, self.angle)

        # --- stage machine ---
        if self.angle > DOWN_ANGLE:
            if self.stage == "up":
                # Completed a full rep
                self.counter += 1
                # Score this rep
                up_score   = max(0, 100 - max(0, self._min_angle_rep - UP_ANGLE) * 3)
                down_score = max(0, 100 - max(0, DOWN_ANGLE - self._max_angle_rep) * 3)
                self.scores.append(round((up_score + down_score) / 2))
                print(f"  {self.name} Rep {self.counter} | "
                      f"peak={self._min_angle_rep:.0f}° "
                      f"ext={self._max_angle_rep:.0f}° "
                      f"score={self.scores[-1]}")
                # Reset per-rep trackers
                self._min_angle_rep = 180.0
                self._max_angle_rep = 0.0
            self.stage = "down"

        elif self.angle < UP_ANGLE:
            self.stage = "up"

    @property
    def score(self) -> int:
        return round(np.mean(self.scores)) if self.scores else 0

    def reset(self):
        self.counter = 0
        self.stage   = None
        self._buf.clear()
        self.scores  = []


# ── HUD drawing ──────────────────────────────────────────────────────────────

def draw_panel(frame, x, y, label, value, color=(0, 255, 100), w=170, h=65):
    """Draw a semi-transparent info panel."""
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), (15, 15, 20), -1)
    cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)
    cv2.putText(frame, label, (x + 8, y + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (160, 160, 170), 1)
    cv2.putText(frame, str(value), (x + 8, y + 54),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, color, 2)


def draw_hud(frame, right: ArmTracker, left: ArmTracker, active_arm: str):
    h, w = frame.shape[:2]
    # Top row — Right arm
    draw_panel(frame,  10, 10, "RIGHT REPS", right.counter, right.color)
    draw_panel(frame, 190, 10, "R STAGE",    right.stage or "---", right.color)
    draw_panel(frame, 370, 10, "R ANGLE",    f"{right.angle:.0f}°", right.color)

    # Second row — Left arm
    draw_panel(frame,  10, 85, "LEFT REPS",  left.counter,  left.color)
    draw_panel(frame, 190, 85, "L STAGE",    left.stage or "---",  left.color)
    draw_panel(frame, 370, 85, "L ANGLE",    f"{left.angle:.0f}°",  left.color)

    # Right column — Score + active arm
    total_score = round((right.score + left.score) / 2) if (right.scores or left.scores) else 0
    draw_panel(frame, 550, 10, "SCORE",  f"{total_score}/100", (200, 130, 255))
    draw_panel(frame, 550, 85, "ACTIVE", active_arm,           (255, 180, 50))

    # Footer
    cv2.putText(frame, "AI Gym Trainer — Bicep Curl (Both Arms) | Q to quit",
                (10, h - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (140, 140, 150), 1)

    # Highlight active arm border
    border_color = right.color if active_arm == "RIGHT" else left.color
    cv2.rectangle(frame, (0, 0), (w - 1, h - 1), border_color, 2)


# ── Landmark extraction ──────────────────────────────────────────────────────

def get_coords(landmarks, landmark_id, w, h):
    """Return pixel (x, y) for a landmark. Returns None if visibility < 0.5."""
    lm = landmarks[landmark_id.value]
    if lm.visibility < 0.5:
        return None
    return [lm.x * w, lm.y * h]


# ── Main loop ────────────────────────────────────────────────────────────────

def run():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)

    right_tracker = ArmTracker("RIGHT", (0, 255, 100))
    left_tracker  = ArmTracker("LEFT",  (100, 200, 255))
    active_arm    = "RIGHT"

    # Track movement magnitude per arm to auto-select active arm
    right_prev_angle = 90.0
    left_prev_angle  = 90.0
    right_movement   = 0.0
    left_movement    = 0.0

    print("\n AI Gym Trainer started. Perform bicep curls in front of the camera.")
    print("  Press Q to quit.\n")

    with mp_pose.Pose(
        min_detection_confidence=0.65,
        min_tracking_confidence=0.65,
        model_complexity=1,
    ) as pose:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Cannot read from webcam. Check connection or try VideoCapture(1).")
                break

            frame = cv2.flip(frame, 1)   # mirror
            ih, iw = frame.shape[:2]

            # MediaPipe inference
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb.flags.writeable = False
            results = pose.process(rgb)
            rgb.flags.writeable = True

            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark

                # Process each arm
                for arm_name, arm_def in ARMS.items():
                    tracker = right_tracker if arm_name == "RIGHT" else left_tracker

                    s = get_coords(lm, arm_def["shoulder"], iw, ih)
                    e = get_coords(lm, arm_def["elbow"],    iw, ih)
                    w_pt = get_coords(lm, arm_def["wrist"],    iw, ih)

                    if s and e and w_pt:
                        raw_angle = calculate_angle(s, e, w_pt)
                        tracker.update(raw_angle)

                        # Draw angle at elbow
                        ex, ey = int(e[0]), int(e[1])
                        cv2.circle(frame, (ex, ey), 8, arm_def["color"], -1)
                        cv2.putText(frame, f"{tracker.angle:.0f}",
                                    (ex - 25, ey - 18),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                    arm_def["color"], 2)

                # Auto-detect active arm (higher angle delta = more movement)
                right_movement = abs(right_tracker.angle - right_prev_angle)
                left_movement  = abs(left_tracker.angle  - left_prev_angle)
                right_prev_angle = right_tracker.angle
                left_prev_angle  = left_tracker.angle

                if right_movement > 3 or left_movement > 3:
                    active_arm = "RIGHT" if right_movement >= left_movement else "LEFT"

                # Draw skeleton
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(80, 80, 90),   thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(160, 160, 180), thickness=2, circle_radius=2),
                )

            draw_hud(frame, right_tracker, left_tracker, active_arm)
            cv2.imshow("FitAI — Gym Trainer", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\n Session ended.")
    print(f"  RIGHT: {right_tracker.counter} reps | score {right_tracker.score}/100")
    print(f"  LEFT:  {left_tracker.counter} reps  | score {left_tracker.score}/100")


if __name__ == "__main__":
    run()