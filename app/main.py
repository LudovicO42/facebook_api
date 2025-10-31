from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

client = MongoClient("xxx")
db = client["facebook_api"]

app = FastAPI(title="Facebook Event API")

class User(BaseModel):
    prenom: str
    nom: str
    email: EmailStr
    password: str
    photo_profil: Optional[str] = None
    date_inscription: Optional[datetime] = datetime.utcnow()

@app.post("/users")
def create_user(user: User):
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    data = user.dict()
    db.users.insert_one(data)
    return {"message": "Utilisateur créé avec succès", "data": data}

@app.get("/users")
def get_users():
    users = list(db.users.find())
    for u in users:
        u["_id"] = str(u["_id"])
    return {"users": users}

@app.get("/")
def root():
    return {"message": "Facebook Event API - en développement"}
