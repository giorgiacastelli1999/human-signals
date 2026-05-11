from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy import Boolean

Base = declarative_base()

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)

    text = Column(String)

    mood = Column(Integer)
    stress = Column(Integer)
    energy = Column(Integer)

    sleep_hours = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)
    exercised = Column(Boolean)
    met_friends = Column(Boolean)
    listened_music = Column(Boolean)
    worked_late = Column(Boolean)
    meditated = Column(Boolean)
    spent_time_outside = Column(Boolean)