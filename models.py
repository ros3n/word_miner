from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Text, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)

    def __str__(self):
        return '{0}: {1}'.format(self.id, self.name)


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

    def __str__(self):
        return '{0}: {1}'.format(self.id, self.title)



if __name__ == '__main__':
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///db.sqlite')

    from sqlalchemy.orm import sessionmaker
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
