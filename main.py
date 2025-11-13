import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Any, Dict

from schemas import User, Workout, Meal, Weightentry
from database import create_document, get_documents, db

app = FastAPI(title="Health & Fitness Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Health & Fitness Tracker Backend Running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but error: {str(e)[:80]}"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# -------- Workouts --------
@app.post("/api/workouts")
def create_workout(workout: Workout):
    try:
        doc_id = create_document("workout", workout)
        return {"id": doc_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/workouts")
def list_workouts(limit: int | None = 50):
    try:
        docs = get_documents("workout", limit=limit)
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------- Meals --------
@app.post("/api/meals")
def create_meal(meal: Meal):
    try:
        doc_id = create_document("meal", meal)
        return {"id": doc_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/meals")
def list_meals(limit: int | None = 50):
    try:
        docs = get_documents("meal", limit=limit)
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------- Weights --------
@app.post("/api/weights")
def create_weight(entry: Weightentry):
    try:
        doc_id = create_document("weightentry", entry)
        return {"id": doc_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weights")
def list_weights(limit: int | None = 50):
    try:
        docs = get_documents("weightentry", limit=limit)
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------- Schemas for UI helpers --------
class SchemaItem(BaseModel):
    name: str
    fields: Dict[str, Any]

@app.get("/schema")
def get_schema() -> List[SchemaItem]:
    return [
        {"name": "user", "fields": User.model_json_schema()["properties"]},
        {"name": "workout", "fields": Workout.model_json_schema()["properties"]},
        {"name": "meal", "fields": Meal.model_json_schema()["properties"]},
        {"name": "weightentry", "fields": Weightentry.model_json_schema()["properties"]},
    ]

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
