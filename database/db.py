from sqlalchemy import create_engine, Column, BigInteger, MetaData, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

engine = create_engine("sqlite+pysqlite:///:memory:")
metadata_obj = MetaData()

class UserIdTable(Base):
    __tablename__ = "user_id"
    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    data_create = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

Session = sessionmaker(engine)

session = Session()