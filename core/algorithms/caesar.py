from core.resources.alphabet import ALPHABET


class CaesarCipher:
    """Алгоритм шифрования Цезаря."""

    def encrypt(self, text: str, key: int) -> str:
        code = ""

        for symbol in text:
            index = ALPHABET.index(symbol)
            new_index = (index + int(key)) % len(ALPHABET)
            code += ALPHABET[new_index]

        return code

    def decrypt(self, text: str, key: int) -> str:
        result = ""

        for symbol in text:
            index = ALPHABET.index(symbol)
            new_index = (index - int(key)) % len(ALPHABET)
            result += ALPHABET[new_index]

        return result