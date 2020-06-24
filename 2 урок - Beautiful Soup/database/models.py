from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    String,
    Integer,
)

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


assoc_article_tag = Table(
    'article_tag',
    Base.metadata,
    Column('article', Integer, ForeignKey('article.id')),
    Column('tag', Integer, ForeignKey('tag.id')),
)


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    created_at = Column(String)
    web_link = Column(String, unique=True)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship('Author', backref='articles')
    tags = relationship('Tag', secondary=assoc_article_tag, backref='articles')

    def __init__(self, title: str, created_at: str, web_link: str, author, tags=[]):
        self.title = title
        self.created_at = created_at
        self.web_link = web_link
        self.author = author
        if tags:
            self.tags.extend(tags)


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    web_link = Column(String, unique=True)

    def __init__(self, name: str, web_link: str):
        self.name = name
        self.web_link = web_link


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    web_link = Column(String, unique=True)

    def __init__(self, name: str, web_link: str):
        self.name = name
        self.web_link = web_link
