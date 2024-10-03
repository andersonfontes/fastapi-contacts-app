from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Contacts App!"}

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = models.User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/contacts/")
def create_contact(name: str, phone: str, email: str, user_id: int, db: Session = Depends(get_db)):
    contact = models.Contact(name=name, phone=phone, email=email, user_id=user_id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact