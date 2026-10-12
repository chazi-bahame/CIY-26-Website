from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    image = Column(String, nullable=False)

class Gallery(Base):
    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    image = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    image = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

class Event(Base):

    __tablename__ = "events"

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)

    description = Column(String, nullable=False)

    event_date = Column(DateTime, nullable=False)

    image = Column(String, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.now
    )


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_read = Column(Integer, default=0)

class JoinApplication(Base):
    __tablename__ = "join_applications"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    email = Column(String, nullable=False)

    password = Column(String, nullable=False)

    phone = Column(String, nullable=False)

    skill = Column(String, nullable=False)

    message = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.now)

    status = Column(String, default="Pending")
