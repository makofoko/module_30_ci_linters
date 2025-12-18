from sqlalchemy import Column, Integer, String, Float, Date, create_engine, func, case
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date

Base = declarative_base()
engine = create_engine("sqlite:///library.db", echo=True)


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer)


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    dormitory = Column(Integer)
    avg_grade = Column(Float)

    @classmethod
    def with_dormitory(cls, session):
        return session.query(cls).filter(cls.dormitory == 1).all()

    @classmethod
    def with_avg_grade_above(cls, session, threshold):
        return session.query(cls).filter(cls.avg_grade > threshold).all()


class ReceivingBooks(Base):
    __tablename__ = "receiving_books"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    book_id = Column(Integer)
    date_receiving = Column(Date)
    date_return = Column(Date, nullable=True)

    @hybrid_property
    def count_date_with_book(self):
        if self.date_return:
            return (self.date_return - self.date_receiving).days
        return (date.today() - self.date_receiving).days

    @count_date_with_book.expression
    def count_date_with_book(cls):
        return case(
            [
                (cls.date_return != None, func.julianday(cls.date_return) - func.julianday(cls.date_receiving))
            ],
            else_=func.julianday(func.current_date()) - func.julianday(cls.date_receiving)
        )


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Таблицы созданы в library.db")