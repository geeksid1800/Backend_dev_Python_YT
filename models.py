from enum import unique

from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    #By default, passing a string parameter will cause it to be interpreted as a string, quotes and all. 
    #If you want to pass a string without quotes, you can use the text() construct. So this will lead to a DDL statment like:
    # created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(), so that it is interpreted as a function instead of a string
    user_id = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"), nullable=False)
    user = relationship("User")
    #"User" references that we want to return an object of class User (ie a particular user). It fetches an object based on the PK-FK relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    def __repr__(self) -> str: 
        return f" id={self.id} email={self.email} created_at={self.created_at}"
    

class Like(Base):
    __tablename__ = "likes"
    user_id = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id',ondelete="CASCADE"), primary_key=True, nullable=False)