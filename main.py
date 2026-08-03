import  ui.configuration
from datetime import datetime

from kivy.app import App

from core.algorithms.algorithm_factory import AlgorithmFactory
from core.enums.algorithm_type import AlgorithmType
from core.enums.operation_mode import OperationMode
from core.models.operation import Operation
from core.models.settings import Settings
from core.services.validator import Validator
from core.storage.history_manager import HistoryManager
from core.storage.settings_manager import SettingsManager


class LockXApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Менеджеры хранения данных
        self.settings_manager = SettingsManager()
        self.history_manager = HistoryManager()

        # Загружаем сохранённые настройки
        self.settings = self.settings_manager.load()

        # Загружаем историю операций
        self.history = self.history_manager.load()

    def build(self):
        """
        Создание интерфейса приложения.
        Kivy загрузит main.kv.
        """
        return super().build()

    def encrypt_or_decrypt(self, text: str) -> str:
        """
        Шифрует или расшифровывает переданный текст
        с использованием текущих настроек.
        """

        # Проверяем исходный текст
        if not Validator.validate_text(text):
            raise ValueError("Текст содержит недопустимые символы.")

        # Проверяем ключ
        if not Validator.validate_key(
            self.settings.algorithm,
            self.settings.key
        ):
            raise ValueError("Некорректный ключ.")

        # Получаем нужный алгоритм
        algorithm = AlgorithmFactory.create(
            self.settings.algorithm
        )

        # Выполняем операцию
        if self.settings.mode == OperationMode.ENCRYPT:
            result = algorithm.encrypt(
                text,
                self.settings.key
            )
        else:
            result = algorithm.decrypt(
                text,
                self.settings.key
            )

        # Создаём запись истории
        operation = Operation(
            source_text=text,
            result_text=result,
            key=self.settings.key,
            algorithm=self.settings.algorithm,
            mode=self.settings.mode,
            created_at=datetime.now()
        )

        # Добавляем операцию в историю
        self.history_manager.add(operation)

        # Обновляем локальную историю
        self.history.append(operation)

        return result

    def update_settings(
        self,
        algorithm: AlgorithmType | None = None,
        mode: OperationMode | None = None,
        key: str | None = None
    ) -> None:
        """
        Изменяет настройки приложения и сохраняет их.
        """

        if algorithm is not None:
            self.settings.algorithm = algorithm

        if mode is not None:
            self.settings.mode = mode

        if key is not None:
            self.settings.key = key

        self.settings_manager.save(self.settings)

    def get_history(self) -> list[Operation]:
        """
        Возвращает историю операций.
        """
        return self.history

    def clear_history(self) -> None:
        """
        Очищает историю операций.
        """
        self.history_manager.clear()
        self.history.clear()


if __name__ == "__main__":
    LockXApp().run()




