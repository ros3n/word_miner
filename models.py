from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Text, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship(
        Author,
        backref=backref('books',
                         uselist=True,
                         cascade='delete,all'))
    contents = Column(Text)



if __name__ == '__main__':
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///db.sqlite')

    from sqlalchemy.orm import sessionmaker
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
