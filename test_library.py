import pytest
from library import Library, Book

@pytest.fixture
def library(tmp_path):
    temp_file = tmp_path / "test_library.json"
    return Library(data_file=str(temp_file))

def test_add_book(library):
    library.add_book("Test Book", "Author A", 2023)
    assert len(library.books) == 1
    assert library.books[0].title == "Test Book"
    assert library.books[0].author == "Author A"
    assert library.books[0].year == 2023

def test_remove_book(library):
    library.add_book("Book to Remove", "Author B", 2022)
    book_id = library.books[0].id
    library.remove_book(book_id)
    assert len(library.books) == 0

def test_remove_nonexistent_book(library, capsys):
    library.remove_book(999)
    captured = capsys.readouterr()
    assert "Книга с id 999 не найдена." in captured.out

def test_search_books_by_title(library, capsys):
    library.add_book("Python Basics", "Author C", 2021)
    library.add_book("Advanced Python", "Author D", 2020)
    library.search_books("Python", "title")
    captured = capsys.readouterr()
    assert "Python Basics" in captured.out
    assert "Advanced Python" in captured.out

def test_search_books_by_author(library, capsys):
    library.add_book("Book One", "Author E", 2019)
    library.add_book("Book Two", "Author E", 2018)
    library.search_books("Author E", "author")
    captured = capsys.readouterr()
    assert "Book One" in captured.out
    assert "Book Two" in captured.out

def test_display_books(library, capsys):
    library.add_book("Book for Display", "Author F", 2017)
    library.display_books()
    captured = capsys.readouterr()
    assert "Book for Display" in captured.out

def test_change_status(library):
    library.add_book("Status Test", "Author G", 2016)
    book_id = library.books[0].id
    library.change_status(book_id, "выдана")
    assert library.books[0].status == "выдана"

def test_change_status_invalid(library, capsys):
    library.add_book("Invalid Status", "Author H", 2015)
    book_id = library.books[0].id
    library.change_status(book_id, "invalid_status")
    captured = capsys.readouterr()
    assert "Неверный статус" in captured.out

def test_find_book_by_id(library):
    library.add_book("Find Me", "Author I", 2014)
    book_id = library.books[0].id
    book = library.find_book_by_id(book_id)
    assert book is not None
    assert book.title == "Find Me"

def test_find_book_by_invalid_id(library):
    book = library.find_book_by_id(12345)
    assert book is None
