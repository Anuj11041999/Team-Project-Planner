from sqlalchemy import Column, Identity, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import datetime
from session import Session
Base = declarative_base()
session = Session()

class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, Identity(start=42, cycle=True), primary_key=True)    
    name = Column(String(64), unique = True)
    display_name = Column(String(128))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def as_dict(self):
       return {"name": self.name, "display_name": self.display_name, "created_at": str(self.created_at), "id": self.id}

    def __repr__(self):
        return f"Users(id={self.id!r}, name={self.name!r}, display_name={self.display_name!r}, created_at={self.created_at})"


class Teams(Base):
    __tablename__ = "Teams"
    id = Column(Integer, Identity(start=42, cycle=True), primary_key=True)    
    description = Column(String(128))
    name = Column(String(64), unique = True)
    admin = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def as_dict(self):
        admin_name = session.get(Users, self.admin).display_name
        return {"name": self.name, "description": self.description, "admin" : admin_name, "created_at": str(self.created_at), "id": self.id}

    def __repr__(self):
        return f"Teams(id={self.id!r}, description={self.description!r}, name={self.name!r}, admin={self.admin!r}, created_at={self.created_at},user={self.user})"

class TeamMembers(Base):
    __tablename__ = "TeamMembers"
    id = Column(Integer, Identity(start=42, cycle=True), primary_key=True)    
    user = Column(Integer, ForeignKey("Users.id"), nullable=False)
    team = Column(Integer, ForeignKey("Teams.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"TeamsMembers(id={self.id!r}, user={self.user}, team={self.team}, created_at={self.created_at})"


class Board(Base):
    __tablename__ = "Board"
    id = Column(Integer, Identity(start=42, cycle=True), primary_key=True)    
    description = Column(String)
    name = Column(String(30), unique = True)
    team = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def as_dict(self):
       return {"name": self.name, "description": self.description, "status" : self.status, "team": self.team, "created_at": str(self.created_at), "id": self.id}

    def __repr__(self):
        return f"Board(description={self.description!r}, name={self.name!r}, status={self.status!r}, created_at={self.created_at}, user={self.user}, team={self.team})"


class Task(Base):
    __tablename__ = "Task"
    id = Column(Integer, Identity(start=42, cycle=True), primary_key=True)    
    description = Column(String)
    title = Column(String(30))
    user = Column(Integer, ForeignKey("Users.id"), nullable=False)
    board = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return f"Task(description={self.description!r}, title={self.title!r}, status={self.status!r}, created_at={self.created_at}, user={self.user})"

