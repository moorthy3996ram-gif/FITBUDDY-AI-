from .ai_client import generate_text, model_name
from .gemini_generator import fallback_plan
from .safety import SAFETY_NOTE

def update_workout_plan(original_plan, feedback, age, weight, goal, intensity):
    prompt = f'''Revise this FitBuddy 7-day wellness plan based on the user's feedback.
Profile: age {age}, weight {weight} kg, goal {goal}, intensity {intensity}.
Original plan:
{original_plan}

Feedback:
{feedback}

Return a complete Day 1–7 plan. Address the feedback while preserving useful parts.
Do not diagnose, prescribe treatment, promise results, or introduce unsafe extremes.
Safety note: {SAFETY_NOTE}'''
    try: return generate_text(prompt, model_name("pro"))
    except Exception:
        return fallback_plan(age, weight, goal, intensity) + f"\n\nFeedback incorporated in fallback mode: {feedback}"
