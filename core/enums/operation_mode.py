from enum import Enum


class OperationMode(Enum):
    """Режим работы приложения."""

    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"