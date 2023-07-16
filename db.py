"""db.py is responsible for handling all database operations."""

from sqlmodel import SQLModel, create_engine, Session, select
from models.command import Command

DATABASE_URL = "sqlite:///.data.db"
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    """Generate the sqlite instance if it does not exist."""
    SQLModel.metadata.create_all(engine)


def create_commands():
    """Create the bot commands and their sample data."""
    with Session(engine) as session:
        # Define a list of command items
        command_items = [
            {
                "name": "guild daily",
                "description": "Retrieve a daily report of Mythic+ Runs "
                "completed so far",
                "usage": "/guild daily",
                "example_image_url": "./images/daily_guild_report.webp",
            },
            {
                "name": "guild weekly",
                "description": "Retrieve a weekly report of Mythic+ Runs "
                "completed so far",
                "usage": "/guild weekly",
                "example_image_url": "./images/weekly_guild_report.webp",
            },
            {
                "name": "guild item_level",
                "description": "Retrieve a leaderboard of the characters "
                "with the 10 highest item levels.",
                "usage": "/guild item_level",
                "example_image_url": "./images/guild_item_level.webp",
            },
            {
                "name": "guild mythic_plus",
                "description": "Retrieve a leaderboard of the characters "
                "with the 10 highest Mythic+ scores by character.",
                "usage": "/guild mythic_plus",
                "example_image_url": "./images/guild_mythic_plus.webp",
            },
            {
                "name": "character best_runs",
                "description": "Retrieve the best runs for a given character.",
                "usage": "/character best_runs <name> <realm>",
                "example_image_url": "./images/character_best.webp",
            },
            {
                "name": "character recent_runs",
                "description": "Retrieve the recent runs for a given character.",
                "usage": "/character recent_runs <name> <realm>",
                "example_image_url": "./images/character_recent.webp",
            },
            # Add more command items as needed
        ]

        # Iterate over the list of command items and create Command instances
        for item in command_items:
            command = Command(**item)
            session.add(command)
        session.commit()

        # Query the database to get the list of inserted commands
        commands = session.query(Command).all()
    return commands


def select_command_by_name(command_name: str):
    """Select a specific command by name."""
    with Session(engine) as session:
        command = session.exec(
            select(Command).where(Command.name == command_name)
        ).first()

    return command


def select_commands():
    """Select all commands."""
    with Session(engine) as session:
        commands = session.exec(select(Command)).fetchall()

    return commands
