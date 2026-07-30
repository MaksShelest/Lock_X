from core.resources.alphabet import ALPHABET


class AuthorsCipher:
    """
    Авторский алгоритм шифрования.

    На данном этапе содержит существующую реализацию,
    адаптированную под новую архитектуру.
    Позже алгоритм будет полностью переработан.
    """

    def encrypt(self, text: str, key: str) -> str:
        """
        Шифрование текста.

        Parameters
        ----------
        text : str
            Исходный текст.

        key : str
            Ключ.

        Returns
        -------
        str
            Зашифрованный текст.
        """

        raise NotImplementedError(
            "Перенос старой реализации будет выполнен на следующем шаге."
        )

    def decrypt(self, text: str, key: str) -> str:
        """
        Расшифрование текста.
        """

        raise NotImplementedError(
            "Перенос старой реализации будет выполнен на следующем шаге."
        )