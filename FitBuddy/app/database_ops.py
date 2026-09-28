from sqlalchemy.orm import Session
from .models import User, Plan

def save_user(db: Session, data):
    user = db.get(User, data.user_id)
    if user:
        user.username, user.age, user.weight, user.goal, user.intensity = data.username, data.age, data.weight, data.goal, data.intensity
    else:
        user = User(id=data.user_id, username=data.username, age=data.age, weight=data.weight, goal=data.goal, intensity=data.intensity)
        db.add(user)
    db.commit(); db.refresh(user); return user

def save_plan(db: Session, user_id: str, original_plan: str, nutrition_tip: str):
    plan = db.query(Plan).filter(Plan.user_id == user_id).first()
    if plan:
        plan.original_plan, plan.nutrition_tip, plan.updated_plan, plan.feedback = original_plan, nutrition_tip, None, None
    else:
        plan = Plan(user_id=user_id, original_plan=original_plan, nutrition_tip=nutrition_tip); db.add(plan)
    db.commit(); db.refresh(plan); return plan

def update_plan(db: Session, user_id: str, updated_plan: str, feedback: str):
    plan = db.query(Plan).filter(Plan.user_id == user_id).first()
    if not plan: return None
    plan.updated_plan, plan.feedback = updated_plan, feedback
    db.commit(); db.refresh(plan); return plan

def get_user(db: Session, user_id: str): return db.get(User, user_id)
def get_plan(db: Session, user_id: str): return db.query(Plan).filter(Plan.user_id == user_id).first()
def get_all_users(db: Session): return db.query(User).order_by(User.created_at.desc()).all()

def delete_user(db: Session, user_id: str):
    user = db.get(User, user_id)
    if not user: return False
    db.delete(user); db.commit(); return True
