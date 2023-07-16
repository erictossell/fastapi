from sqlmodel import SQLModel, create_engine, Session, select
from models.item import Item
from models.command import Command

DATABASE_URL = "sqlite:///.test.db"
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_example_item():
    with Session(engine) as session:
        item = Item(name="Foo", description="This is an item")
        session.add(item)
        session.commit()
    return item


def create_commands():
    with Session(engine) as session:
        # Define a list of command items
        command_items = [
            {
                "name": "guild daily",
                "description": "Retrieve a daily report of Mythic+ Runs completed so far",
                "usage": "/guild daily",
                "example_image_url": "./images/daily_guild_report.png",
            },
            {
                "name": "guild weekly",
                "description": "Retrieve a weekly report of Mythic+ Runs completed so far",
                "usage": "/guild weekly",
                "example_image_url": "./images/weekly_guild_report.png",
            },
            {
                "name": "guild item_level",
                "description": "Retrieve a leaderboard of the characters with the 10 highest item levels.",
                "usage": "/guild item_level",
                "example_image_url": "./images/guild_item_level.png",
            },
            {
                "name": "guild mythic_plus",
                "description": "Retrieve a leaderboard of the characters with the 10 highest Mythic+ scores by character.",
                "usage": "/guild mythic_plus",
                "example_image_url": "./images/guild_mythic_plus.png",
            },
            {
                "name": "character best_runs",
                "description": "Retrieve the best runs for a given character.",
                "usage": "/character best_runs <name> <realm>",
                "example_image_url": "./images/character_best.png",
            },
            {
                "name": "character recent_runs",
                "description": "Retrieve the recent runs for a given character.",
                "usage": "/character recent_runs <name> <realm>",
                "example_image_url": "./images/character_recent.png",
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


def select_item_by_name(item_name: str):
    with Session(engine) as session:
        item = session.exec(select(Item).where(Item.name == item_name)).first()
    return item


def select_command_by_name(command_name: str):
    with Session(engine) as session:
        command = session.exec(
            select(Command).where(Command.name == command_name)
        ).first()

    return command


def select_commands():
    with Session(engine) as session:
        commands = session.exec(select(Command)).fetchall()

    return commands
