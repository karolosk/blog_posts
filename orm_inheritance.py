from sqlalchemy import Column, String, create_engine, event, DDL, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

conn_string = "postgres://user:pwd@localhost:5432/code_examples"
db = create_engine(conn_string, echo=True)
Base = declarative_base()

event.listen(
    Base.metadata, "before_create", DDL("CREATE SCHEMA IF NOT EXISTS orm_inheritance")
)


class BaseModel(Base):
    __abstract__ = True  # declared to not be created by create_all
    __table_args__ = {"schema": "orm_inheritance"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)

    def save(self, session, commit=True):
        session.add(self)
        if commit:
            try:
                session.commit()
            except Exception as e:
                session.rollback()
            finally:
                session.close()


class Class(BaseModel):
    __tablename__ = "class"

    name = Column(String)
    description = Column(String)


class Teacher(BaseModel):
    __tablename__ = "teacher"

    name = Column(String)
    surname = Column(String)
    hired_at = Column(DateTime)


class Student(BaseModel):
    __tablename__ = "student"

    name = Column(String)
    surname = Column(String)
    birth_date = Column(DateTime)


if __name__ == "__main__":
    Session = sessionmaker(db)
    session = Session()

    Base.metadata.create_all(db)
