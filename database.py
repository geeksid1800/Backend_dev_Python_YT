from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import urllib

db_pass = urllib.parse.quote_plus(settings.db_password, safe="")
SQLALCHEMY_DATABASE_URL = f"{settings.db_type}://{settings.db_username}:{db_pass}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"
 # "Database_Type://Username:Password@<IP/Hostname>/Database_Name"
engine = create_engine(SQLALCHEMY_DATABASE_URL) #establishes a connection

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #SessionLocal is not a Session object itself. It is a Factory class that can be used to manufacture Session objects.

Base = declarative_base() #All tables are represented as models/classes in SQLAlchemy, and they all inherit from this class.

def get_db():
    #Create a session object that can be used to interact with the database. 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()