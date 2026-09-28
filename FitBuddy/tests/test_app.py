import os, tempfile
from pathlib import Path
DB=Path(tempfile.gettempdir())/"fitbuddy_test.db"
if DB.exists(): DB.unlink()
os.environ["DATABASE_URL"]=f"sqlite:///{DB}"
os.environ["GOOGLE_API_KEY"]=""
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
init_db()
client=TestClient(app)

def test_home():
    r=client.get('/'); assert r.status_code==200; assert 'FitBuddy' in r.text

def test_generation_and_feedback():
    r=client.post('/generate-workout',data={'username':'Test User','user_id':'test001','age':'25','weight':'70','goal':'general wellness','intensity':'medium'})
    assert r.status_code==200; assert 'FITBUDDY 7-DAY WORKOUT PLAN' in r.text
    r=client.post('/submit-feedback',data={'user_id':'test001','feedback':'Add more cardio and another recovery day.'})
    assert r.status_code==200; assert 'updated workout plan' in r.text.lower()

def test_api():
    r=client.get('/api/users/test001'); assert r.status_code==200; assert r.json()['user']['user_id']=='test001'
