from abc import ABC, abstractmethod


class State(ABC):
    """
    Интерфейс Состояния объявляет методы, которые должны реализовать все
    конкретные состояния. Эти методы соответствуют действиям, которые может
    выполнять контекст в зависимости от текущего состояния.
    """

    @abstractmethod
    def handle(self) -> None:
        pass #исправить


class ConcreteStateA(State):
    """
    Конкретные состояния реализуют поведение, связанное с определенным
    состоянием контекста. Каждое состояние может самостоятельно определять,
    в какое состояние переходить дальше.
    """

    def handle(self) -> None:
        print("ConcreteStateA: Обработка запроса.")
        # Логика перехода в другое состояние
        # self._context.change_state(ConcreteStateB())


class ConcreteStateB(State):
    """
    Другое конкретное состояние с альтернативным поведением.
    """

    def handle(self) -> None:
        print("ConcreteStateB: Обработка запроса по-другому.")


class Context:
    """
    Контекст хранит ссылку на объект текущего состояния и делегирует ему все
    операции. Контекст может самостоятельно менять свое состояние в процессе
    работы.
    """

    def __init__(self, state: State) -> None:
        """
        Контекст инициализируется с начальным состоянием. Начальное состояние
        может быть передано извне или установлено по умолчанию.
        """
        self._state = state

    def change_state(self, state: State) -> None:
        """
        Метод для смены текущего состояния контекста.
        """
        print(f"Context: Смена состояния на {state.__class__.__name__}")
        self._state = state

    def request(self) -> None:
        """
        Контекст делегирует выполнение запроса текущему состоянию. В зависимости
        от результата, контекст может самостоятельно сменить состояние.
        """
        self._state.handle()


def client_code(context: Context) -> None:
    """
    Клиентский код должен работать с контекстом через его публичный интерфейс.
    Контекст сам управляет своими состояниями, клиенту не нужно знать о
    конкретных классах состояний.
    """

    context.request()


if __name__ == "__main__":
    print("Client: Executing client code with initial state A:")
    initial_state = ConcreteStateA()
    context = Context(initial_state)
    client_code(context)

    print("\nClient: Changing state manually:")
    context.change_state(ConcreteStateB())
    client_code(context)
