from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import (
    Base,
    Article,
    Author,
    Tag,
)


class ArticleDB:
    def __init__(self, path: str, base=Base):
        engine = create_engine(path)
        base.metadata.create_all(engine)
        session_db = sessionmaker(bind=engine)
        self.__session = session_db()

    @property
    def session(self):
        return self.__session


if __name__ == '__main__':
    db_path = 'sqlite:///article.sqlite'
    db = ArticleDB(db_path)
    print(1)