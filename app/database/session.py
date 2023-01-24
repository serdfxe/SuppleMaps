from sqlalchemy.orm import sessionmaker
from app.database import engine


Session = sessionmaker(bind=engine)
