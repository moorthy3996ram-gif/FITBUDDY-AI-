from pathlib import Path
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import get_db
from .database_ops import *
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan
from .schemas import UserInput, FeedbackRequest

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
router = APIRouter()

def render_result(request, user, plan, message=None):
    return templates.TemplateResponse("result.html", {"request":request,"user":user,"plan":plan,"message":message})

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(request: Request, username: str=Form(...), user_id: str=Form(...), age: int=Form(...), weight: float=Form(...), goal: str=Form(...), intensity: str=Form(...), db: Session=Depends(get_db)):
    try:
        data=UserInput(username=username,user_id=user_id,age=age,weight=weight,goal=goal,intensity=intensity.lower())
    except Exception as exc:
        return templates.TemplateResponse("index.html", {"request":request,"error":str(exc)}, status_code=422)
    user=save_user(db,data)
    workout=generate_workout_gemini(data.age,data.weight,data.goal,data.intensity)
    tip=generate_nutrition_tip_with_flash(data.goal)
    plan=save_plan(db,user.id,workout,tip)
    return render_result(request,user,plan)

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: str=Form(...), feedback: str=Form(...), db: Session=Depends(get_db)):
    try: data=FeedbackRequest(user_id=user_id,feedback=feedback)
    except Exception as exc: raise HTTPException(422,str(exc))
    user=get_user(db,data.user_id); plan=get_plan(db,data.user_id)
    if not user or not plan: raise HTTPException(404,"User or workout plan not found")
    updated=update_workout_plan(plan.original_plan,data.feedback,user.age,user.weight,user.goal,user.intensity)
    plan=update_plan(db,user.id,updated,data.feedback)
    return render_result(request,user,plan,"Your updated workout plan has been saved.")

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, db: Session=Depends(get_db)):
    return templates.TemplateResponse("all_users.html", {"request":request,"users":get_all_users(db)})

@router.get("/api/users")
def api_users(db: Session=Depends(get_db)):
    return JSONResponse([{"user_id":u.id,"username":u.username,"age":u.age,"weight":u.weight,"goal":u.goal,"intensity":u.intensity,"created_at":u.created_at.isoformat()} for u in get_all_users(db)])

@router.get("/api/users/{user_id}")
def api_user(user_id: str, db: Session=Depends(get_db)):
    user=get_user(db,user_id)
    if not user: raise HTTPException(404,"User not found")
    plan=get_plan(db,user_id)
    return {"user":{"user_id":user.id,"username":user.username,"age":user.age,"weight":user.weight,"goal":user.goal,"intensity":user.intensity},"plan":None if not plan else {"original_plan":plan.original_plan,"updated_plan":plan.updated_plan,"feedback":plan.feedback,"nutrition_tip":plan.nutrition_tip}}

@router.delete("/api/users/{user_id}")
def api_delete_user(user_id: str, db: Session=Depends(get_db)):
    if not delete_user(db,user_id): raise HTTPException(404,"User not found")
    return {"message":"User deleted","user_id":user_id}
