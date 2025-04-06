from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

url_to_db = "postgresql://daria_h:mysecretpassword123@localhost:5432/postgres"
engine = create_engine(url_to_db)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
