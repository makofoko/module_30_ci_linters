from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, create_engine, func, case, event
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import date
import re

Base = declarative_base()
engine = create_engine("sqlite:///library.db", echo=True)

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan", lazy="joined")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books", lazy="subquery")
    receiving_books = relationship("ReceivingBooks", back_populates="book", cascade="all, delete-orphan")
    students = association_proxy("receiving_books", "student")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    dormitory = Column(Integer)
    avg_grade = Column(Float)
    phone = Column(String)
    receiving_books = relationship("ReceivingBooks", back_populates="student", cascade="all, delete-orphan", lazy="joined")
    books = association_proxy("receiving_books", "book")

class ReceivingBooks(Base):
    __tablename__ = "receiving_books"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    date_receiving = Column(Date)
    date_return = Column(Date, nullable=True)

    student = relationship("Student", back_populates="receiving_books")
    book = relationship("Book", back_populates="receiving_books")

    @hybrid_property
    def count_date_with_book(self):
        if self.date_return:
            return (self.date_return - self.date_receiving).days
        return (date.today() - self.date_receiving).days

    @count_date_with_book.expression
    def count_date_with_book(cls):
        return case(
            [(cls.date_return != None, func.julianday(cls.date_return) - func.julianday(cls.date_receiving))],
            else_=func.julianday(func.current_date()) - func.julianday(cls.date_receiving)
        )

# 🔹 ORM Event: проверка телефона
phone_pattern = re.compile(r"^\+7\(9\d{2}\)-\d{3}-\d{2}-\d{2}$")

@event.listens_for(Student, "before_insert")
def validate_phone(mapper, connection, target):
    if not phone_pattern.match(target.phone):
        raise ValueError("Неверный формат телефона")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Таблицы созданы в library.db")