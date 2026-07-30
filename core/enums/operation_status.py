from enum import Enum


class OperationStatus(Enum):
    """Статус выполнения операции."""

    SUCCESS = "success"
    ERROR = "error"