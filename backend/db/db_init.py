import logging
from sqlmodel import SQLModel
from backend.config.session import async_engine, get_async_session
from backend.db.db_models import User
from backend.db.db_crud import create_record, read_record
from backend.db.db_excepts import RecordNotFound


async def init_db() -> None:
    """Initialize database and load admin user."""
    try:
        # [Emergency drop all in case db schema doesn't update]
        # async with async_engine.begin() as conn:
        #     await conn.run_sync(SQLModel.metadata.drop_all)

        # Create all tables
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
            logging.info("Database tables created successfully")

        # Load admin user
        success = await load_admin()
        if not success:
            logging.error("Failed to load admin user")

    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        raise


async def load_admin() -> bool:
    """
    Load or create admin user in database.
    Returns True if successful, False otherwise.
    """
    try:
        async with get_async_session() as session:
            try:
                admin = await read_record(session, User, 1)
            except RecordNotFound:
                logging.info("Admin user not found, creating new admin user")
                admin = User(
                    username="admin",
                    email="admin@admin.com",
                    role="admin",
                    status="active",
                    login_token="Not needed",
                    token_expiry=0,
                )
                await create_record(session, admin)
                logging.info("Admin user created successfully")
                return True

            logging.info("Admin user already exists")
            return True

    except Exception as e:
        logging.error(f"Error loading admin user: {e}")
        return False
