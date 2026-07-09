from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = "mysql+pymysql://root:123456@localhost:3306/BTTH1_SS13"

engine = create_engine(DB_URL)

localSession = sessionmaker(
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    autocommit = False
)

def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()