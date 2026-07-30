from core.resources.alphabet import ALPHABET


class VigenerCipher:
    """Алгоритм шифрования Виженера."""

    def encrypt(self, text: str, key: str) -> str:
        key_stream = []

        for i in range(len(text)):
            key_stream.append(key[i % len(key)])

        result = ""

        for i in range(len(text)):
            text_index = ALPHABET.index(text[i])
            key_index = ALPHABET.index(key_stream[i])

            result_index = (text_index + key_index) % len(ALPHABET)
            result += ALPHABET[result_index]

        return result

    def decrypt(self, text: str, key: str) -> str:
        key_stream = []

        for i in range(len(text)):
            key_stream.append(key[i % len(key)])

        result = ""

        for i in range(len(text)):
            text_index = ALPHABET.index(text[i])
            key_index = ALPHABET.index(key_stream[i])

            result_index = (text_index - key_index) % len(ALPHABET)
            result += ALPHABET[result_index]

        return result