from .ai_client import generate_text, model_name
from .safety import SAFETY_NOTE

def fallback_tip(goal):
    return (f"For {goal}, aim for balanced meals with a protein source, fruit/vegetables, "
            f"whole-food carbohydrates, healthy fats, regular hydration and adequate sleep. {SAFETY_NOTE}")

def generate_nutrition_tip_with_flash(goal):
    prompt = f'''Give one concise practical nutrition or recovery tip for the fitness goal "{goal}".
Keep it general wellness guidance, avoid restrictive diets and medical claims, and stay under 80 words.
Safety note: {SAFETY_NOTE}'''
    try: return generate_text(prompt, model_name("flash"))
    except Exception: return fallback_tip(goal)
