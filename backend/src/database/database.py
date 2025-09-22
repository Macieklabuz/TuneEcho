from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from contextlib import contextmanager

DATABASE_URL = "sqlite:///data/songs.db"  # plik songs.db w katalogu projektu

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()



# ----- INIT -----
def init_db():
    Base.metadata.create_all(bind=engine)

# Context manager na sesje
@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
