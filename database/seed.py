"""
Populate the database with sample data from CSV files.
"""
import pandas as pd
from sqlalchemy.orm import Session
from database.database import engine, SessionLocal
from database.schema import Base, User, Company, Event, Application, ActivityLog, RetentionMetric
from config.config import DATA_DIR
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_csv(filename: str):
    """Load CSV from data directory."""
    path = DATA_DIR / filename
    if not path.exists():
        logger.warning(f"CSV file not found: {path}")
        return None
    return pd.read_csv(path)

def seed_database():
    """Create tables and populate with sample data."""
    logger.info("Creating tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        # Load CSVs
        users_df = load_csv("users.csv")
        companies_df = load_csv("companies.csv")
        events_df = load_csv("events.csv")
        applications_df = load_csv("applications.csv")
        activity_logs_df = load_csv("activity_logs.csv")
        retention_df = load_csv("retention.csv")

        if companies_df is not None:
            logger.info("Seeding companies...")
            companies_df.to_sql("companies", con=engine, if_exists="append", index=False)

        if users_df is not None:
            logger.info("Seeding users...")
            users_df.to_sql("users", con=engine, if_exists="append", index=False)

        if events_df is not None:   # FIXED: was "not_right"
            logger.info("Seeding events...")
            events_df.to_sql("events", con=engine, if_exists="append", index=False)

        if applications_df is not None:
            logger.info("Seeding applications...")
            applications_df.to_sql("applications", con=engine, if_exists="append", index=False)

        if activity_logs_df is not None:
            logger.info("Seeding activity logs...")
            activity_logs_df.to_sql("activity_logs", con=engine, if_exists="append", index=False)

        if retention_df is not None:
            logger.info("Seeding retention metrics...")
            retention_df.to_sql("retention", con=engine, if_exists="append", index=False)

        session.commit()
        logger.info("Database seeded successfully.")
    except Exception as e:
        session.rollback()
        logger.error(f"Error seeding database: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()