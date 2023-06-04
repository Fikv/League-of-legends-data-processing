from sqlalchemy import create_engine
from Base import Base

engine = create_engine('postgresql://postgres:postgres@localhost:5432/LOL_DATA2')
Base.metadata.create_all(engine)