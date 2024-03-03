"""main.py is responsible for handling all requests and returning a response."""
# pylint: disable=E0611
from pydantic import BaseModel

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db import (
    create_commands,
    create_db_and_tables,
    select_command_by_name,
    select_commands,
)

create_db_and_tables()
create_commands()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://mplusbot.up.railway.app",
        "https://www.mythicplusbot.dev",
    ],  # Allow CORS from React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/images", StaticFiles(directory="images"), name="images")


# pylint: disable=C0115,R0903
class Msg(BaseModel):
    msg: str


# pylint: disable=C0116
@app.get("/")
async def root():
    return {"message": "Hello, you've found the default root of the MplusAPI!"}


@app.get("/command/{name}")
async def read_command(name: str):
    """Return a specific command's details."""
    command = select_command_by_name(name)
    if command is None:
        return {"error": "Item not found"}
    image_url = f"https://mplus-api.up.railway.app/{command.example_image_url}"
    return {
        "id": command.id,
        "name": command.name,
        "description": command.description,
        "usage": command.usage,
        "image_url": image_url,
    }


@app.get("/command/")
async def read_all_commands():
    """Return all command names in a list."""
    commands = select_commands()
    if commands is None:
        return {"error": "Item not found"}
    return {"commands": [command.name for command in commands]}
