from sqlalchemy import create_engine, event, DDL
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

conn_string = "db_uri"
db = create_engine(conn_string, echo=True)
Base = declarative_base()

event.listen(
    Base.metadata, "before_create", DDL("CREATE SCHEMA IF NOT EXISTS orm_example")
)


class Test(Base):
    __tablename__ = "test"
    __table_args__ = {"schema": "orm_example"}

    title = Column(String, primary_key=True)


Session = sessionmaker(db)
session = Session()

Base.metadata.create_all(db)

new_entry = Test(title="hello")

session.add(new_entry)
session.commit()
