from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from database.database import Base


# Define the Posts table
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    post_url = Column(String(2048), unique=True, nullable=False)
    user_name = Column(String(255), unique=False, nullable=True)
    user_url = Column(String(2048), unique=False, nullable=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)

    # Relationships
    matches = relationship("Match", back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, user_name={self.user_name})>"


# Define the Searches table
class Search(Base):
    __tablename__ = 'searches'

    id = Column(Integer, primary_key=True)  # Changed from String to Integer
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # Can be user, company, topic, or job
    usernames = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)  # String to store keywords or usernames
    notify = Column(Boolean, default=False)

    matches = relationship("Match")

    def __repr__(self):
        return f"<Search(id={self.id}, name='{self.name}', type='{self.type}')>"


# Define the Matches table
class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    search_id = Column(Integer, ForeignKey('searches.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    matched_at = Column(DateTime, nullable=False)

    posts = relationship("Post", back_populates="matches")
    searches = relationship("Search", back_populates="matches")

    def __repr__(self):
        return f"<Match(id={self.id}, search_id={self.search_id}, post_id={self.post_id}, matched_at={self.matched_at})>"
