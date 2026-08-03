import json
from pathlib import Path

from core.enums.algorithm_type import AlgorithmType
from core.enums.operation_mode import OperationMode
from core.models.settings import Settings


class SettingsManager:
    """Менеджер сохранения и загрузки настроек приложения."""

    def __init__(self, file_path: str = "data/settings.json"):
        self.file_path = Path(file_path)

    def load(self) -> Settings:
        """Загружает настройки из файла."""

        if not self.file_path.exists():
            settings = Settings()
            self.save(settings)
            return settings

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            return Settings(
                algorithm=AlgorithmType(data["algorithm"]),
                mode=OperationMode(data["mode"]),
                key=data["key"]
            )

        except (json.JSONDecodeError, KeyError, ValueError):
            settings = Settings()
            self.save(settings)
            return settings

    def save(self, settings: Settings) -> None:
        """Сохраняет настройки в файл."""

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                {
                    "algorithm": settings.algorithm.value,
                    "mode": settings.mode.value,
                    "key": settings.key
                },
                file,
                ensure_ascii=False,
                indent=4
            )