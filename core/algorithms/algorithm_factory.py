from core.algorithms.caesar import CaesarCipher
from core.algorithms.vigener import VigenerCipher
from core.algorithms.authors import AuthorsCipher

from core.enums.algorithm_type import AlgorithmType


class AlgorithmFactory:
    """Фабрика создания алгоритмов шифрования."""

    @staticmethod
    def create(algorithm_type: AlgorithmType):
        match algorithm_type:
            case AlgorithmType.CAESAR:
                return CaesarCipher()

            case AlgorithmType.VIGENER:
                return VigenerCipher()

            case AlgorithmType.AUTHORS:
                return AuthorsCipher()

            case _:
                raise ValueError(
                    f"Неизвестный алгоритм: {algorithm_type}"
                )