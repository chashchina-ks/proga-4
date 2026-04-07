# Пример шаблона проектирования "Состояние" на Python

from abc import ABC, abstractmethod
from typing import Literal


# 1. Абстрактное состояние (интерфейс)
class IState(ABC):
    @abstractmethod
    def play(self) -> str:
        pass

    @abstractmethod
    def pause(self) -> str:
        pass

    @abstractmethod
    def stop(self) -> str:
        pass


# 2. Конкретные состояния

class PlayingState(IState):
    def play(self) -> str:
        return "уже играет"

    def pause(self) -> str:
        return "поставлен на паузу"

    def stop(self) -> str:
        return "остановлен"


class PausedState(IState):
    def play(self) -> str:
        return "возобновляет воспроизведение"

    def pause(self) -> str:
        return "уже на паузе"

    def stop(self) -> str:
        return "остановлен с паузы"


class StoppedState(IState):
    def play(self) -> str:
        return "начинает воспроизведение"

    def pause(self) -> str:
        return "нельзя поставить на паузу - сначала нажмите Play"

    def stop(self) -> str:
        return "уже остановлен"


# 3. Контекст (объект, который меняет свое поведение)
class MediaPlayer:
    def __init__(self, initial_state: IState) -> None:
        self._state = initial_state

    def change_state(self, state: IState) -> None:
        self._state = state

    def play(self) -> str:
        result = self._state.play()
        # Если состояние позволяет, меняем его
        if result == "начинает воспроизведение":
            self.change_state(PlayingState())
        elif result == "возобновляет воспроизведение":
            self.change_state(PlayingState())
        return f"Плеер {result}"

    def pause(self) -> str:
        result = self._state.pause()
        if result == "поставлен на паузу":
            self.change_state(PausedState())
        return f"Плеер {result}"

    def stop(self) -> str:
        result = self._state.stop()
        if result == "остановлен" or result == "остановлен с паузы":
            self.change_state(StoppedState())
        return f"Плеер {result}"


def create_player(state_name: Literal["playing", "paused", "stopped"]) -> MediaPlayer:
    if state_name == "playing":
        return MediaPlayer(PlayingState())
    elif state_name == "paused":
        return MediaPlayer(PausedState())
    elif state_name == "stopped":
        return MediaPlayer(StoppedState())
    else:
        raise ValueError("Unknown state")


# 5. Демонстрация работы
if __name__ == "__main__":

    # Создаем плеер в начальном состоянии "остановлен"
    player = create_player("stopped")

    print("\n--- Сценарий 1: Нормальное воспроизведение ---")
    print(player.play())    # Остановлен -> Играет
    print(player.pause())   # Играет -> Пауза
    print(player.play())    # Пауза -> Играет
    print(player.stop())    # Играет -> Остановлен

    print("\n--- Сценарий 2: Некорректные действия ---")
    print(player.stop())    # Остановлен -> Остановлен (ошибка)
    print(player.pause())   # Остановлен -> Пауза (ошибка)
    print(player.play())    # Остановлен -> Играет (нормально)

    print("\n--- Сценарий 3: Смена состояний через фабрику ---")
    player2 = create_player("playing")
    print(f"Начальное состояние: играет")
    print(player2.pause())
    print(player2.stop())

    print("\n--- Сценарий 4: Проверка всех состояний ---")
    for state in ["playing", "paused", "stopped"]:
        print(f"\nСтарт с состоянием: {state}")
        test_player = create_player(state)
        print(f"  {test_player.play()}")
        print(f"  {test_player.pause()}")
        print(f"  {test_player.stop()}")
