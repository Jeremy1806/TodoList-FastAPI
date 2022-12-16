from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv('environ/.env')

db_url = os.environ['HOST']


engine = create_engine(db_url)
session_local = sessionmaker(bind=engine , expire_on_commit=False)
 
    
