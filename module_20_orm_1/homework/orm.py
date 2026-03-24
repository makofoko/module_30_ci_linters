from init_db import Base, engine, Author, Book, Student, ReceivingBooks
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

author1 = Author(name="Лев Толстой")
author2 = Author(name="Фёдор Достоевский")

book1 = Book(title="Война и мир", author=author1)
book2 = Book(title="Преступление и наказание", author=author2)

student1 = Student(name="Мағжан", dormitory=1, avg_grade=4.5)
student2 = Student(name="Айжан", dormitory=0, avg_grade=3.8)

rb1 = ReceivingBooks(student=student1, book=book1, date_receiving=date.today() - timedelta(days=20))
rb2 = ReceivingBooks(student=student2, book=book2, date_receiving=date.today() - timedelta(days=5))

session.add_all([author1, author2, book1, book2, student1, student2, rb1, rb2])
session.commit()

print("База инициализирована тестовыми данными")