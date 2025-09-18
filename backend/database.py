import os
from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, BigInteger, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Ścieżka do SQLite z ENV (ustawimy ją w docker-compose)
DB_URL = os.getenv("DB_PATH", "sqlite:///fingerprints.db")  # lokalnie: ./fingerprints.db

engine = create_engine(DB_URL, future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    artist = Column(String)
    album = Column(String)
    file_path = Column(String, nullable=False)  # ścieżka/URL do pliku
    duration = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    fingerprints = relationship("Fingerprint", back_populates="song", cascade="all, delete-orphan")

class Fingerprint(Base):
    __tablename__ = "fingerprints"
    id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False, index=True)
    hash = Column(BigInteger, nullable=False, index=True)
    t_anchor = Column(Integer, nullable=False)
    song = relationship("Song", back_populates="fingerprints")

def init_db():
    Base.metadata.create_all(engine)

@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
