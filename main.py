from sqlalchemy import select

from fastapi import FastAPI, Depends

from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.schemas import UserRead, UserCreate
from auth.database import User, create_db_and_tables, drop_db_and_tables, async_session_maker
from auth.manager import get_user_manager
from contextlib import asynccontextmanager

from typing import Annotated

from schemas import SNoteAdd, SNote
from auth.database import Note

import requests

@asynccontextmanager
async def lifespan(app: FastAPI):
    # print("Drop tables")
    # await drop_db_and_tables()
    print("Create tables")
    await create_db_and_tables()
    yield



app = FastAPI(
    title="App",
    lifespan=lifespan
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()

def check_text(text: str) -> str:
    url = "https://speller.yandex.net/services/spellservice.json/checkText"

    params = {
        "text": text
    }
    response = requests.get(url, params=params)

    result = response.json()

    for elem in result:
        text = text[:elem['col']] + elem['s'][0] + text[elem['col'] + elem['len']:]

    return text



@app.post("/note")
async def create_note(
        note: Annotated[SNoteAdd, Depends()],
        user: User = Depends(current_user),
    ) -> SNote:

    finish_text = check_text(note.text)

    async with async_session_maker() as session:
        note_dict = note.model_dump()
        note_dict['text'] = finish_text

        note_instans = Note(**note_dict, user_id=user.id)
        session.add(note_instans)
        await session.flush()
        await session.commit()
        return note_instans

@app.get("/todo")
async def get_notes(
        user: User = Depends(current_user),
    ) -> list[SNote]:
    async with async_session_maker() as session:
        query = select(Note).where(Note.user_id == user.id)
        result = await session.execute(query)
        note_models = result.scalars().all()
        note_schemas = [SNote.model_validate(note_model) for note_model in note_models]
        return note_schemas


