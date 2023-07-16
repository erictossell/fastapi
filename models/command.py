"""command.py is a simple model for the database layer."""
from sqlmodel import SQLModel, Field


# pylint: disable=too-few-public-methods
class Command(SQLModel, table=True):
    """The command model."""

    id: int = Field(default=None, primary_key=True)
    name: str = Field()
    description: str = Field(default=None, nullable=True)
    usage: str = Field(default=None, nullable=True)
    example_image_url: str = Field(default=None, nullable=True)
