from .ai_client import generate_text, model_name
from .safety import SAFETY_NOTE

def fallback_plan(age, weight, goal, intensity):
    return f'''FITBUDDY 7-DAY WORKOUT PLAN
Profile: age {age}, weight {weight:g} kg, goal: {goal}, intensity: {intensity.capitalize()}

Day 1 – Full Body
Warm-up: 5–10 min easy movement.
Main: Squat 3x10; incline push-up 3x8; glute bridge 3x12; bird dog 3x8/side.
Cooldown: 5 min easy walking and mobility.

Day 2 – Cardio + Core
Warm-up: 5–10 min.
Main: Brisk walk/cycle 20–30 min; dead bug 3x8/side; plank 3x20–30 sec.
Cooldown: 5 min easy movement.

Day 3 – Recovery
20–30 min comfortable walking plus gentle full-body mobility.

Day 4 – Upper Body
Warm-up: 5–10 min.
Main: Incline push-up 3x8; band row 3x10; shoulder rotation 2x12; light carry 3x30 sec.
Cooldown: Gentle mobility.

Day 5 – Lower Body
Warm-up: 5–10 min.
Main: Squat 3x10; supported split squat 2x8/side; glute bridge 3x12; calf raise 3x12.
Cooldown: Gentle mobility.

Day 6 – Conditioning
20–30 min moderate cardio with comfortable intervals; optional light core circuit.

Day 7 – Rest / Active Recovery
Rest, easy walking, or gentle mobility.

{SAFETY_NOTE}'''

def generate_workout_gemini(age, weight, goal, intensity):
    prompt = f'''You are FitBuddy, a conservative wellness and fitness planning assistant.
Create a practical structured 7-day workout plan for age {age}, weight {weight} kg, goal {goal}, intensity {intensity}.
Include Day 1–7, warm-up, main work with sets/reps or duration, cooldown/recovery and rest days.
Do not diagnose, prescribe treatment, promise results, or recommend unsafe extremes.
If a movement may be difficult, include a simpler alternative.
End with this safety note: {SAFETY_NOTE}'''
    try: return generate_text(prompt, model_name("pro"))
    except Exception: return fallback_plan(age, weight, goal, intensity)
