"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: db.py
Description: Database utils

"""

import os
import uuid
from sqlalchemy import Column, String, Float, Integer, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class MemoryUnitDB(Base):
    __tablename__ = "memory_units"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    type = Column(String)
    depth = Column(Float)
    content = Column(String)
    keywords = Column(String)
    created = Column(Integer, default=0)
    last_accessed = Column(Integer, default=0)
    score = Column(Float, default=0.0)


class SqliteDB:
    def __init__(self, db_name):
        self.db_name = db_name

        self.db_path = os.path.join(os.getcwd(), "sqlite_db", f"{self.db_name}.db")
        if not os.path.exists(os.path.dirname(self.db_path)):
            os.makedirs(os.path.dirname(self.db_path))

        self.engine = create_engine(f"sqlite:///{self.db_path}")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        Base.metadata.create_all(self.engine)

    def query_memory_by_type(self, type: MemoryUnitDB.type, n_results: int):
        return (
            self.session.query(MemoryUnitDB)
            .filter(MemoryUnitDB.type == type)
            .order_by(MemoryUnitDB.created.desc())
            .limit(n_results)
            .all()
        )

    def insert_memory(self, memory: MemoryUnitDB):
        self.session.add(memory)
        self.session.commit()
