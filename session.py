from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///db/task_management.db', echo=True)

Session = sessionmaker(bind=engine)
