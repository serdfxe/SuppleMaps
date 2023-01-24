from sqlalchemy.engine import create_engine

from sqlalchemy.orm import declarative_base

import app.settings as settings


engine = create_engine(settings.DATABASE_URL)
Base = declarative_base(bind=engine)
