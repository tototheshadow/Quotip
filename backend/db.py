from sqlmodel import SQLModel, create_engine

# sqlite_file_name = "hanyamalam.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
sqlite_url = "mysql+pymysql://hariyangcerah:hoshikara@34.101.221.48/mcr"

# connect_args = {"check_same_thread": False}
# engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)