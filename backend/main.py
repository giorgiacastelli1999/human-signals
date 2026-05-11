from fastapi import FastAPI
from pydantic import BaseModel
from db import SessionLocal
from models import JournalEntry

app = FastAPI()

class JournalEntryCreate(BaseModel):
    text: str
    mood: int
    stress: int
    energy: int
    sleep_hours: float
    exercised: bool
    met_friends: bool
    listened_music: bool
    worked_late: bool
    meditated: bool
    spent_time_outside: bool

@app.get("/")
def root():
    return {"message": "HumanSignals API running"}

@app.post("/entries")
def create_entry(entry: JournalEntryCreate):

    db = SessionLocal()

    new_entry = JournalEntry(
        text=entry.text,
        mood=entry.mood,
        stress=entry.stress,
        energy=entry.energy,
        sleep_hours=entry.sleep_hours,
        exercised=entry.exercised,
        met_friends=entry.met_friends,
        listened_music=entry.listened_music,
        worked_late=entry.worked_late,
        meditated=entry.meditated,
        spent_time_outside=entry.spent_time_outside

    )

    db.add(new_entry)
    db.commit()

    return {"message": "Entry created successfully"}

@app.get("/entries")
def get_entries():

    db = SessionLocal()

    entries = db.query(JournalEntry).all()

    results = []

    for entry in entries:
        results.append({
            "id": entry.id,
            "text": entry.text,
            "mood": entry.mood,
            "stress": entry.stress,
            "energy": entry.energy,
            "sleep_hours": entry.sleep_hours,
            "exercised": entry.exercised,
            "met_friends": entry.met_friends,
            "listened_music": entry.listened_music,
            "worked_late": entry.worked_late,
            "meditated": entry.meditated,
            "spent_time_outside": entry.spent_time_outside,
            "created_at": str(entry.created_at)
        })

    return results