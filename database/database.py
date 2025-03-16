from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


# Create a base class for our models
Base = declarative_base()


# Database setup function
def setup_database(db_path='sqlite:///linkedin_data.db') -> tuple[Engine, sessionmaker[Session]]:
    """
    Set up the database connection and create tables if they don't exist.

    Args:
        db_path (str): Database connection string. Defaults to SQLite database in the current directory.

    Returns:
        tuple: (engine, session_maker) - SQLAlchemy engine and session maker objects
    """
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return engine, session
