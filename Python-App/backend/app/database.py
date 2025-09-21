from sqlmodel import SQLModel, create_engine, Session
from .config import settings

# checks if the database URL starts with 'sqlite' - if so, it sets the connect_args to false - needed for database when using environment with web servers
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
# engine is created to establish the connection to the database specified by the DATABASE_URL - echo=False argument disables SQL query logging and connect_args passes needed connection options
engine = create_engine(settings.DATABASE_URL, echo=False, connect_args=connect_args)

# initializes the db schema - creates all tables defined in the SQLModel if they dont already exist
def init_db():
    SQLModel.metadata.create_all(engine)

# yields a new database session- by using the context manager (line 15), it makes sure the session is properly closed after use
# used commonly for fastAPI to provide a session to each request in an efficient way
def get_session():
    with Session(engine) as session:
        yield session