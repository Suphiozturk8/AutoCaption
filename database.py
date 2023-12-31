
import os, threading, asyncio

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, Column, Integer, String

from config import DB_URL


def start() -> scoped_session:
    engine = create_engine(
        DB_URL,
        client_encoding="utf8"
    )
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(
        sessionmaker(
            bind=engine,
            autoflush=False
        )
    )


BASE = declarative_base()
SESSION = start()

INSERTION_LOCK = threading.RLock()

class custom_button(BASE):
    __tablename__ = "button"
    id = Column(Integer, primary_key=True)
    button = Column(String)

    def __init__(self, id, button):
        self.id = id
        self.button = button

custom_button.__table__.create(checkfirst=True)

class custom_caption(BASE):
    __tablename__ = "caption"
    id = Column(Integer, primary_key=True)
    caption = Column(String)

    def __init__(self, id, caption):
        self.id = id
        self.caption = caption

custom_caption.__table__.create(checkfirst=True)

async def update_caption(id, caption):
    with INSERTION_LOCK:
        cap = SESSION.query(custom_caption).get(id)
        if not cap:
            cap = custom_caption(id, caption)
            SESSION.add(cap)
            SESSION.flush()
        else:
            SESSION.delete(cap)
            cap = custom_caption(id, caption)
            SESSION.add(cap)
        SESSION.commit()

async def del_caption(id):
    with INSERTION_LOCK:
        msg = SESSION.query(custom_caption).get(id)
        SESSION.delete(msg)
        SESSION.commit()

async def get_caption(id):
    try:
        caption = SESSION.query(custom_caption).get(id)
        return caption
    finally:
        SESSION.close()

async def update_button(id, button):
    with INSERTION_LOCK:
        btn = SESSION.query(custom_button).get(id)
        if not btn:
            btn = custom_button(id, button)
            SESSION.add(btn)
            SESSION.flush()
        else:
            SESSION.delete(btn)
            btn = custom_button(id, button)
            SESSION.add(btn)
        SESSION.commit()

async def del_button(id):
    with INSERTION_LOCK:
        msg = SESSION.query(custom_button).get(id)
        SESSION.delete(msg)
        SESSION.commit()

async def get_button(id):
    try:
        button = SESSION.query(custom_button).get(id)
        return button
    finally:
        SESSION.close()
