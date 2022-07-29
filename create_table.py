from tables import Base
from session import engine

Base.metadata.create_all(engine)
