from __future__ import annotations
"""
Database Schemas for Health & Fitness Tracker

Each Pydantic model represents a collection in your database.
Collection name is the lowercase of the class name.
"""
from pydantic import BaseModel, Field
from typing import Optional
import datetime as dt

class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    age: Optional[int] = Field(None, ge=0, le=120)
    height_cm: Optional[float] = Field(None, ge=0)
    is_active: bool = Field(True)

class Workout(BaseModel):
    date: dt.date = Field(..., description="Workout date (YYYY-MM-DD)")
    workout_type: str = Field(..., description="Workout type e.g., Running, Yoga, Strength")
    duration_minutes: int = Field(..., ge=1, le=1440, description="Duration in minutes")
    calories_burned: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None

class Meal(BaseModel):
    date: dt.date = Field(...)
    meal_type: str = Field(..., description="Breakfast, Lunch, Dinner, Snack")
    calories: int = Field(..., ge=0)
    protein_g: Optional[float] = Field(None, ge=0)
    carbs_g: Optional[float] = Field(None, ge=0)
    fat_g: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None

class Weightentry(BaseModel):
    date: dt.date = Field(...)
    weight_kg: float = Field(..., ge=0)
    notes: Optional[str] = None
