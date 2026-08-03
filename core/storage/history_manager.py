import json
from pathlib import Path
from datetime import datetime

from core.enums.algorithm_type import AlgorithmType
from core.enums.operation_mode import OperationMode
from core.models.operation import Operation


class HistoryManager:
    """Менеджер истории операций."""

    def __init__(self, file_path: str = "data/history.json"):
        self.file_path = Path(file_path)

    def load(self) -> list[Operation]:
        """Загружает историю операций."""

        if not self.file_path.exists():
            self.save([])
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            operations = []

            for item in data:
                operations.append(
                    Operation(
                        source_text=item["source_text"],
                        result_text=item["result_text"],
                        key=item["key"],
                        algorithm=AlgorithmType(item["algorithm"]),
                        mode=OperationMode(item["mode"]),
                        created_at=datetime.fromisoformat(
                            item["created_at"]
                        )
                    )
                )

            return operations

        except (json.JSONDecodeError, KeyError, ValueError, TypeError):
            self.save([])
            return []

    def save(self, operations: list[Operation]) -> None:
        """Сохраняет историю операций."""

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        data = []

        for operation in operations:
            data.append(
                {
                    "source_text": operation.source_text,
                    "result_text": operation.result_text,
                    "key": operation.key,
                    "algorithm": operation.algorithm.value,
                    "mode": operation.mode.value,
                    "created_at": operation.created_at.isoformat()
                }
            )

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    def add(self, operation: Operation) -> None:
        """Добавляет новую операцию в историю."""

        operations = self.load()
        operations.append(operation)
        self.save(operations)

    def clear(self) -> None:
        """Полностью очищает историю."""

        self.save([])