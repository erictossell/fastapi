from sqlmodel import SQLModel, Field


class Command(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field()
    description: str = Field(default=None, nullable=True)
    usage: str = Field(default=None, nullable=True)
    example_image_url: str = Field(default=None, nullable=True)
