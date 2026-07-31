from core.enums.algorithm_type import AlgorithmType
from core.resources.alphabet import ALPHABET


class Validator:
    """
    Проверка корректности входных данных.
    """

    @staticmethod
    def validate_text(text: str) -> bool:
        """
        Проверяет, что текст не пустой
        и содержит только допустимые символы.
        """

        if not text:
            return False

        return all(symbol in ALPHABET for symbol in text)

    @staticmethod
    def validate_caesar_key(key: str) -> bool:
        """
        Проверяет ключ для шифра Цезаря.
        """

        if not key.isdigit():
            return False

        key = int(key)

        return 0 <= key < len(ALPHABET)

    @staticmethod
    def validate_vigener_key(key: str) -> bool:
        """
        Проверяет ключ для шифра Виженера.
        """

        if not key:
            return False

        return all(symbol in ALPHABET for symbol in key)

    @staticmethod
    def validate_authors_key(key: str) -> bool:
        """
        Проверяет ключ авторского алгоритма.
        Пока используется такая же логика,
        как и для Виженера.
        """

        return Validator.validate_vigener_key(key)

    @staticmethod
    def validate_key(
        algorithm: AlgorithmType,
        key: str
    ) -> bool:

        if algorithm == AlgorithmType.CAESAR:
            return Validator.validate_caesar_key(key)

        if algorithm == AlgorithmType.VIGENER:
            return Validator.validate_vigener_key(key)

        if algorithm == AlgorithmType.AUTHORS:
            return Validator.validate_authors_key(key)

        return False