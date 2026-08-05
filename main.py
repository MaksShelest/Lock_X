import ui.configuration

from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from core.algorithms.algorithm_factory import AlgorithmFactory
from core.enums.algorithm_type import AlgorithmType
from core.enums.operation_mode import OperationMode
from core.models.operation import Operation
from core.services.validator import Validator
from core.storage.history_manager import HistoryManager
from core.storage.settings_manager import SettingsManager


class LockXApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings_manager = SettingsManager()
        self.history_manager = HistoryManager()

        self.settings = self.settings_manager.load()
        self.history = self.history_manager.load()

    def build(self):
        return Builder.load_file("main.kv")

    def on_start(self):
        """
        Вызывается после создания интерфейса.
        Устанавливает в UI сохранённые настройки.
        """

        self.root.ids.algorithm_spinner.text = (
            self.get_algorithm_name(self.settings.algorithm)
        )

        self.root.ids.mode_spinner.text = (
            self.get_mode_name(self.settings.mode)
        )

        self.root.ids.key_input.text = self.settings.key

    # ==========================================================
    # Преобразование Enum -> название в интерфейсе
    # ==========================================================

    @staticmethod
    def get_algorithm_name(algorithm: AlgorithmType) -> str:
        """Возвращает название алгоритма для интерфейса."""

        names = {
            AlgorithmType.CAESAR: "Цезарь",
            AlgorithmType.VIGENER: "Виженер",
            AlgorithmType.AUTHORS: "Авторский"
        }

        return names[algorithm]

    @staticmethod
    def get_mode_name(mode: OperationMode) -> str:
        """Возвращает название режима для интерфейса."""

        names = {
            OperationMode.ENCRYPT: "Шифрование",
            OperationMode.DECRYPT: "Расшифрование"
        }

        return names[mode]

    # ==========================================================
    # Преобразование названия из интерфейса -> Enum
    # ==========================================================

    @staticmethod
    def get_algorithm_type(name: str) -> AlgorithmType:
        """Преобразует название алгоритма в Enum."""

        algorithms = {
            "Цезарь": AlgorithmType.CAESAR,
            "Виженер": AlgorithmType.VIGENER,
            "Авторский": AlgorithmType.AUTHORS
        }

        return algorithms[name]

    @staticmethod
    def get_operation_mode(name: str) -> OperationMode:
        """Преобразует название режима в Enum."""

        modes = {
            "Шифрование": OperationMode.ENCRYPT,
            "Расшифрование": OperationMode.DECRYPT
        }

        return modes[name]

    # ==========================================================
    # Изменение настроек из UI
    # ==========================================================

    def on_algorithm_changed(self, value: str):
        """Обрабатывает изменение алгоритма."""

        algorithm = self.get_algorithm_type(value)

        self.settings.algorithm = algorithm
        self.settings_manager.save(self.settings)

    def on_mode_changed(self, value: str):
        """Обрабатывает изменение режима."""

        mode = self.get_operation_mode(value)

        self.settings.mode = mode
        self.settings_manager.save(self.settings)

    def on_key_changed(self, value: str):
        """Обрабатывает изменение ключа."""

        self.settings.key = value
        self.settings_manager.save(self.settings)

    # ==========================================================
    # Основная операция
    # ==========================================================

    def encrypt_or_decrypt(self):
        """
        Шифрует или расшифровывает текст из интерфейса.
        """

        text = self.root.ids.text_input.text

        # Синхронизируем настройки с UI
        self.settings.algorithm = self.get_algorithm_type(
            self.root.ids.algorithm_spinner.text
        )

        self.settings.mode = self.get_operation_mode(
            self.root.ids.mode_spinner.text
        )

        self.settings.key = self.root.ids.key_input.text

        # Сохраняем настройки
        self.settings_manager.save(self.settings)

        # Проверяем текст
        if not Validator.validate_text(text):
            self.show_error(
                "Ошибка",
                "Введите текст или используйте только "
                "символы из поддерживаемого алфавита."
            )
            return

        # Проверяем ключ
        if not Validator.validate_key(
            self.settings.algorithm,
            self.settings.key
        ):
            self.show_error(
                "Ошибка",
                "Некорректный ключ для выбранного алгоритма."
            )
            return

        try:
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

        except NotImplementedError:
            self.show_error(
                "Ошибка",
                "Авторский алгоритм пока не реализован."
            )
            return

        except Exception as error:
            self.show_error(
                "Ошибка",
                str(error)
            )
            return

        # Показываем результат
        self.root.ids.text_output.text = result

        # Создаём запись истории
        operation = Operation(
            source_text=text,
            result_text=result,
            key=self.settings.key,
            algorithm=self.settings.algorithm,
            mode=self.settings.mode,
            created_at=datetime.now()
        )

        # Сохраняем операцию
        self.history_manager.add(operation)
        self.history.append(operation)

    # ==========================================================
    # История
    # ==========================================================

    def clear_history(self):
        """Очищает историю операций."""

        self.history_manager.clear()
        self.history.clear()

    # ==========================================================
    # Ошибки
    # ==========================================================

    @staticmethod
    def show_error(title: str, message: str):
        """Показывает пользователю сообщение об ошибке."""

        content = Label(
            text=message,
            halign="center",
            valign="middle"
        )

        content.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.3)
        )

        popup.open()

    def on_stop(self):
        """
        Сохраняем настройки перед закрытием приложения.
        """

        self.settings_manager.save(self.settings)


if __name__ == "__main__":
    LockXApp().run()