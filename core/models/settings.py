from dataclasses import dataclass

from core.enums.algorithm_type import AlgorithmType
from core.enums.operation_mode import OperationMode


@dataclass
class Settings:
    """
    Настройки приложения.
    """

    algorithm: AlgorithmType = AlgorithmType.CAESAR
    mode: OperationMode = OperationMode.ENCRYPT
    key: str = ""