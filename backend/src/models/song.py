
from sqlalchemy import Column, DateTime, Float, Integer, String, func
from database.database import Base
from sqlalchemy.orm import relationship

# ----- MODELE -----
class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    artist = Column(String)
    album = Column(String)
    file_path = Column(String, nullable=False)
    duration = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    fingerprints = relationship("Fingerprint", back_populates="song", cascade="all, delete-orphan")
    