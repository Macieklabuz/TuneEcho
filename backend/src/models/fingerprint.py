from sqlalchemy import Column, DateTime, Float, Integer, String, func, BigInteger, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship

class Fingerprint(Base):
    __tablename__ = "fingerprints"
    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False, index=True)
    hash = Column(BigInteger, nullable=False, index=True)   # fingerprint hash
    t_anchor = Column(Integer, nullable=False)              # czas wystąpienia
    song = relationship("Song", back_populates="fingerprints")