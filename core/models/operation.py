from dataclasses import dataclass
from datetime import datetime

from core.enums.algorithm_type import AlgorithmType
from core.enums.operation_mode import OperationMode


@dataclass
class Operation:
    """
    Описание одной операции шифрования/расшифрования.
    """

    source_text: str
    result_text: str
    key: str

    algorithm: AlgorithmType
    mode: OperationMode

    created_at: datetime