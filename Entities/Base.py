from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


Base = declarative_base()
engine = create_engine('postgresql://postgres:postgres@localhost:5432/lol_data3', connect_args={'dbname': 'lol_data3'})
Base.metadata.create_all(engine)

