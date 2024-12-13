import json
from typing import List, Dict, Optional


class Book:
    """
    Класс для представления книги в библиотеке.

    Атрибуты:
        book_id (int): Уникальный идентификатор книги.
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.
        status (str): Статус книги ("в наличии" или "выдана").
    """

    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        year: int,
        status: str = "в наличии",
    ):
        self.id: int = book_id
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def to_dict(self) -> Dict[str, str | int]:
        """
        Преобразует объект книги в словарь.

        Returns:
            Dict: Словарь, содержащий данные о книге.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: Dict[str, str | int]) -> "Book":
        """
        Создает объект книги из словаря.

        Args:
            data (Dict): Словарь с данными о книге.

        Returns:
            Book: Объект книги.
        """
        return Book(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"],
        )


class Library:
    """
    Класс для управления библиотекой книг.

    Атрибуты:
        data_file (str): Путь к файлу для хранения данных библиотеки.
        books (List[Book]): Список книг в библиотеке.
    """

    def __init__(self, data_file: str = "library.json"):
        self.books: List[Book] = []
        self.data_file: str = data_file
        self.load_books()

    def load_books(self):
        """
        Загружает данные о книгах из файла.
        Если файл не существует или содержит ошибки, список книг остается пустым.
        """
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.books = [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []

    def save_books(self) -> None:
        """
        Сохраняет данные о книгах в файл.
        """
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(
                [book.to_dict() for book in self.books],
                file,
                ensure_ascii=False,
                indent=4,
            )

    def add_book(self, title: str, author: str, year: int):
        """
        Добавляет новую книгу в библиотеку.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
        """
        book_id: int = 1 if not self.books else self.books[-1].id + 1
        new_book: Book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга добавлена: {new_book.title} ({new_book.year})")

    def remove_book(self, book_id: int):
        """
        Удаляет книгу из библиотеки по ее идентификатору.

        Args:
            book_id (int): Идентификатор книги для удаления.
        """
        book: Optional[Book] = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Книга с id {book_id} удалена.")
        else:
            print(f"Книга с id {book_id} не найдена.")

    def search_books(self, keyword: str, field: str):
        """
        Ищет книги по заданному ключевому слову и полю.

        Args:
            keyword (str): Ключевое слово для поиска.
            field (str): Поле для поиска (title, author, year).
        """
        results: List[Book] = [
            book
            for book in self.books
            if keyword.lower() in str(getattr(book, field)).lower()
        ]
        if results:
            self.display_books(results)
        else:
            print(f"Книги по запросу '{keyword}' не найдены.")

    def display_books(self, books: Optional[List[Book]] = None):
        """
        Отображает список книг в библиотеке.

        Args:
            books (Optional[List[Book]]): Список книг для отображения. Если None, отображаются все книги.
        """
        books = books or self.books
        if not books:
            print("Библиотека пуста.")
            return
        for book in books:
            print(
                f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}"
            )

    def change_status(self, book_id: int, new_status: str):
        """
        Изменяет статус книги.

        Args:
            book_id (int): Идентификатор книги.
            new_status (str): Новый статус книги ("в наличии" или "выдана").
        """
        book: Optional[Book] = self.find_book_by_id(book_id)
        if book:
            if new_status in ["в наличии", "выдана"]:
                book.status = new_status
                self.save_books()
                print(f"Статус книги с id {book_id} изменен на '{new_status}'.")
            else:
                print("Неверный статус. Используйте 'в наличии' или 'выдана'.")
        else:
            print(f"Книга с id {book_id} не найдена.")

    def find_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Находит книгу по ее идентификатору.

        Args:
            book_id (int): Идентификатор книги.

        Returns:
            Optional[Book]: Найденная книга или None, если книга не найдена.
        """
        return next((book for book in self.books if book.id == book_id), None)


def main():
    """
    Главная функция для работы с библиотекой через консольное меню.
    """
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            if not title:
                print("Название книги не может быть пустым.")
                continue
            author = input("Введите автора книги: ")

            year = input("Введите год издания книги: ")
            if not year.isdigit():
                year = 0
            else:
                year = int(year)

            library.add_book(title, author, year)
        elif choice == "2":
            try:
                book_id = int(input("Введите id книги для удаления: "))
            except ValueError:
                print("Неверный id")
                continue
            library.remove_book(book_id)
        elif choice == "3":
            field = (
                input("Введите поле для поиска (title, author, year): ").strip().lower()
            )
            keyword = input("Введите ключевое слово для поиска: ")
            library.search_books(keyword, field)
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            try:
                book_id = int(input("Введите id книги: "))
            except ValueError:
                print("Неверный id")
                continue
            new_status = input("Введите новый статус (в наличии/выдана): ")
            library.change_status(book_id, new_status)
        elif choice == "6":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
