from fastapi import FastAPI
from pydantic import BaseModel
from db import (
    create_commands,
    create_db_and_tables,
    create_example_item,
    select_command_by_name,
    select_item_by_name,
    select_commands,
)
from models.item import Item
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

create_db_and_tables()
create_example_item()
create_commands()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://mplusbot.up.railway.app",
    ],  # Allow CORS from React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/images", StaticFiles(directory="images"), name="images")


class Msg(BaseModel):
    msg: str


@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}


@app.get("/item/{name}")
async def read_items(name: str):
    item = select_item_by_name(name)
    if item is None:
        return {"error": "Item not found"}
    return item


@app.get("/command/{name}")
async def read_command(name: str):
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
    commands = select_commands()
    if commands is None:
        return {"error": "Item not found"}
    return {"commands": [command.name for command in commands]}
