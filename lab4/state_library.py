from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional


class IBookState(ABC):
    """
    Интерфейс Состояния книги объявляет методы, которые должны реализовать все
    конкретные состояния. Эти методы соответствуют действиям, которые может
    выполнять читатель с книгой в зависимости от текущего состояния.
    """

    @abstractmethod
    def borrow(self, user: str) -> str:
        """
        Взять книгу на руки.
        """
        raise NotImplementedError("Метод должен быть реализован в подклассе")

    @abstractmethod
    def reserve(self, user: str) -> str:
        """
        Забронировать книгу.
        """
        raise NotImplementedError("Метод должен быть реализован в подклассе")

    @abstractmethod
    def return_book(self, user: str) -> str:
        """
        Вернуть книгу в библиотеку.
        """
        raise NotImplementedError("Метод должен быть реализован в подклассе")

    @abstractmethod
    def extend(self, user: str) -> str:
        """
        Продлить срок сдачи книги.
        """
        raise NotImplementedError("Метод должен быть реализован в подклассе")

    @abstractmethod
    def get_status_description(self) -> str:
        """
        Получить описание текущего состояния книги.
        """
        raise NotImplementedError("Метод должен быть реализован в подклассе")


class AvailableState(IBookState):
    """
    Состояние "В наличии". Книга доступна для выдачи или бронирования.
    Появляется при условии, что книга не у другого человека и не забронирована
    другим пользователем.
    """

    def borrow(self, user: str) -> str:
        return f"Книга выдана пользователю '{user}'. Статус: 'У вас на руках'"

    def reserve(self, user: str) -> str:
        return f"Книга забронирована пользователем '{user}'. Статус: 'Забронировано вами'"

    def return_book(self, user: str) -> str:
        return "Книга уже в библиотеке. Нечего возвращать."

    def extend(self, user: str) -> str:
        return "Нельзя продлить книгу, которую вы не брали."

    def get_status_description(self) -> str:
        return "В наличии"


class UnavailableState(IBookState):
    """
    Состояние "Нет в наличии". Книга выдана другому читателю или забронирована
    другим пользователем.
    """

    def __init__(self, owner: str):
        self._owner = owner

    def borrow(self, user: str) -> str:
        return f"Книга недоступна. В данный момент у пользователя '{self._owner}'."

    def reserve(self, user: str) -> str:
        return f"Книга уже забронирована пользователем '{self._owner}'. Недоступна для бронирования."

    def return_book(self, user: str) -> str:
        return "Книга не у вас на руках. Нечего возвращать."

    def extend(self, user: str) -> str:
        return "Нельзя продлить книгу, которую вы не брали."

    def get_status_description(self) -> str:
        return f"Нет в наличии (у {self._owner})"


class BorrowedByUserState(IBookState):
    """
    Состояние "Уже на руках пользователя". Книга находится у текущего пользователя.
    Появляется при условии, что пользователь уже забрал книгу из библиотеки,
    вне зависимости от того, бронировал он заранее или нет.
    """

    def __init__(self, user: str, borrow_date: datetime):
        self._user = user
        self._borrow_date = borrow_date

    def _get_days_borrowed(self) -> int:
        """Сколько дней книга у пользователя."""
        return (datetime.now() - self._borrow_date).days

    def borrow(self, user: str) -> str:
        return f"Книга уже у вас на руках. Нельзя взять повторно."

    def reserve(self, user: str) -> str:
        return f"Книга уже у вас на руках. Не нужно бронировать."

    def return_book(self, user: str) -> str:
        if user == self._user:
            return f"Книга возвращена пользователем '{user}' в библиотеку."
        return f"Книга не у вас на руках. Вы не можете её вернуть."

    def extend(self, user: str) -> str:
        days = self._get_days_borrowed()
        if user != self._user:
            return "Вы не можете продлить книгу, которая не у вас."
        if days >= 14:
            return "Книга просрочена! Сначала верните книгу, затем возьмите снова."
        return f"Продление невозможно. Книга у вас {days} дней. Продление доступно только на 14-й день."

    def get_status_description(self) -> str:
        days = self._get_days_borrowed()
        if days >= 14:
            return "Можно продлить (или книга просрочена)"
        elif days >= 12:
            return f"У вас на руках (приближается срок сдачи - {14 - days} дня)"
        else:
            return f"У вас на руках (дней с момента выдачи: {days})"


class ReservedByUserState(IBookState):
    """
    Состояние "Забронировано пользователем". Пользователь забронировал книгу,
    но еще не взял её.
    """

    def __init__(self, user: str):
        self._user = user

    def borrow(self, user: str) -> str:
        if user == self._user:
            return f"Бронирование подтверждено. Книга выдана пользователю '{user}'."
        return f"Книга забронирована другим пользователем. Недоступна для выдачи."

    def reserve(self, user: str) -> str:
        if user == self._user:
            return "Книга уже забронирована вами."
        return f"Книга уже забронирована пользователем '{self._user}'."

    def return_book(self, user: str) -> str:
        return "Книга не у вас на руках. Нечего возвращать."

    def extend(self, user: str) -> str:
        return "Нельзя продлить книгу, которую вы ещё не взяли."

    def get_status_description(self) -> str:
        return "Забронировано вами"


class Book:
    """
    Контекст (Книга) хранит ссылку на объект текущего состояния и
    делегирует ему все действия. Контекст может самостоятельно менять
    свое состояние в процессе работы.
    """

    def __init__(self, title: str):
        self._title = title # Название книги
        self._state: IBookState = AvailableState() # Текущее состояние (по умолчанию "В наличии")
        self._current_user: Optional[str] = None # Кто сейчас держит книгу
        self._borrow_date: Optional[datetime] = None # Дата выдачи книги

    def change_state(self, state: IBookState) -> None:
        """Метод для смены текущего состояния книги."""
        print(f"\n{'='*50}")
        print(f"Книга '{self._title}':")
        print(f"Новый статус: {state.get_status_description()}")
        self._state = state

    def borrow(self, user: str) -> None:
        """Взять книгу на руки."""
        result = self._state.borrow(user)

        # Проверяем, нужно ли сменить состояние
        if "выдана пользователю" in result:
            self._current_user = user
            self._borrow_date = datetime.now()
            self.change_state(BorrowedByUserState(user, self._borrow_date))
        elif "Бронирование подтверждено" in result:
            self._current_user = user
            self._borrow_date = datetime.now()
            self.change_state(BorrowedByUserState(user, self._borrow_date))

        print(f"  {result}")

    def reserve(self, user: str) -> None:
        """Забронировать книгу."""
        result = self._state.reserve(user)

        # Проверяем, нужно ли сменить состояние
        if "забронирована пользователем" in result and "вами" in result:
            self.change_state(ReservedByUserState(user))
        elif "забронирована пользователем" in result:
            # Извлекаем имя пользователя из результата
            parts = result.split("'")
            if len(parts) >= 2:
                owner = parts[1]
                self.change_state(UnavailableState(owner))

        print(f"  {result}")

    def return_book(self, user: str) -> None:
        """Вернуть книгу в библиотеку."""
        result = self._state.return_book(user)

        if "возвращена" in result:
            self._current_user = None
            self._borrow_date = None
            self.change_state(AvailableState())

        print(f"  {result}")

    def extend(self, user: str) -> None:
        """Продлить срок сдачи книги."""
        result = self._state.extend(user)

        # Если продление разрешено, обновляем дату выдачи
        if "Продление невозможно" not in result and "Нельзя" not in result:
            if "доступно только на 14-й день" in result:
                pass  # Уже сообщили пользователю
            elif self._borrow_date and isinstance(self._state, BorrowedByUserState):
                # Обновляем дату выдачи при успешном продлении
                self._borrow_date = datetime.now()
                self.change_state(BorrowedByUserState(user, self._borrow_date))
                print(f"Срок сдачи продлен! Новая дата выдачи: {self._borrow_date.strftime('%d.%m.%Y')}")
                return

        print(f"  {result}")

    def get_status(self) -> None:
        """Показать текущий статус книги."""
        print(f"\nКнига: {self._title}")
        print(f"Статус: {self._state.get_status_description()}")


def client_code(book: Book, user: str) -> None:
    """
    Клиентский код демонстрирует пользовательский опыт работы с библиотекой.
    """
    print(f"\nПользователь: {user}")
    print("-" * 50)


if __name__ == "__main__":

    # Создаем книгу
    book = Book("Мастер и Маргарита")
    user = "Алексей"

    # Демонстрация 1: Книга в наличии
    print("\n" + "=" * 50)
    print("\n" + "СЦЕНАРИЙ 1: Книга в наличии")
    book.get_status()
    book.borrow(user)
    book.get_status()

    # Демонстрация 2: Симуляция приближения срока сдачи
    print("\n" + "=" * 50)
    print("\n" + "СЦЕНАРИЙ 2: Приближается срок сдачи (12-й день)")

    # Создаем новую книгу
    book2 = Book("1984")
    user2 = "Мария"

    # Выдаем книгу с датой 12 дней назад
    book2._borrow_date = datetime.now() - timedelta(days=12)
    book2._current_user = user2
    book2.change_state(BorrowedByUserState(user2, book2._borrow_date))
    book2.get_status()

    # Пытаемся продлить (еще нельзя, только на 14-й день)
    print("\n--- Попытка продлить на 12-й день ---")
    book2.extend(user2)

    # Демонстрация 3: Можно продлить (14-й день)
    print("\n" + "=" * 50)
    print("\n" + "СЦЕНАРИЙ 3: Можно продлить (14-й день)")

    book3 = Book("Преступление и наказание")
    user3 = "Иван"

    # Выдаем книгу с датой 14 дней назад
    book3._borrow_date = datetime.now() - timedelta(days=14)
    book3._current_user = user3
    book3.change_state(BorrowedByUserState(user3, book3._borrow_date))
    book3.get_status()

    # Продлеваем
    print("\n--- Попытка продлить на 14-й день ---")
    book3.extend(user3)

    # Демонстрация 4: Бронирование книги
    print("\n" + "=" * 50)
    print("\n" + "СЦЕНАРИЙ 4: Бронирование книги другим пользователем")

    book4 = Book("Война и мир")
    user4a = "Ольга"
    user4b = "Петр"

    book4.get_status()
    book4.reserve(user4a)
    print("\n--- Попытка взять книгу другим пользователем ---")
    book4.borrow(user4b)

    # Демонстрация 5: Возврат книги
    print("\n" + "=" * 50)
    print("\n" + "СЦЕНАРИЙ 5: Возврат книги в библиотеку")

    book5 = Book("Анна Каренина")
    user5 = "Елена"

    book5.borrow(user5)
    book5.get_status()
    book5.return_book(user5)
    book5.get_status()
