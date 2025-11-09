from sqlmodel import SQLModel,create_engine
# from sqlalchemy import create_engine --- IGNORE ---

DATABASE_URL = "mysql+mysqlconnector://root:password@database/appdb"
engine = create_engine(DATABASE_URL)

def get_session():
    from sqlmodel import Session
    with Session(engine) as session:
        yield session