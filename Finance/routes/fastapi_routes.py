from fastapi import APIRouter
from models.chit import Chit
from database.db import Database

fastapi_router = APIRouter()
db = Database()

@fastapi_router.get("/api/chits")
async def get_chits():
    cursor = db.get_connection().cursor(dictionary=True)
    cursor.execute("SELECT * FROM chits")
    chits = cursor.fetchall()
    cursor.close()
    return chits

@fastapi_router.post("/api/chits")
async def create_chit(chit: Chit):
    try:
        cursor = db.get_connection().cursor()
        cursor.execute(
            "INSERT INTO chits (chit_name, amount, duration_months, total_members) VALUES (%s, %s, %s, %s)",
            (chit.chit_name, chit.amount, chit.duration_months, chit.total_members)
        )
        db.get_connection().commit()
        cursor.close()
        return {"message": "Chit created successfully"}
    except Exception as e:
        print(f"Error creating chit: {e}")
        return {"error": "Failed to create chit"}, 500
