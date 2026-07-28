import data
from data import Encryption_type


class Validator:
    def __init__(self, data):
        self.data = data
        pass

    def validate_text(self, text, alphabet): # валидация текста
        valid_text = text
        if self.data.encryption_type == Encryption_type.CAESAR:
            valid_text = text.lower()
        if self._check_alphabet_set(valid_text, alphabet):
            print(f"Validator -> validate_text() -> преобразование текста прошло успешно. Текст: {valid_text}")
            self.data.text = valid_text
        else:
            print(f"Validator -> validate_text() -> текст содержит неразрешенные символы. Текст: {valid_text}")
            self.data.text = ""


    def event_validate_text(self, instance, value):
        self.validate_text(text=value, alphabet=self.data.current_alphabet)

    def event_validate_key(self, instance, value):
        self.validate_key(value)


    def validate_key(self, key):
        max_key_value = len(self.data.current_alphabet) - 1
        if self.data.encryption_type == Encryption_type.CAESAR:
            try:
                valid_key = int(key)
                if valid_key < 0 or valid_key < max_key_value:
                    print(f"Validator -> validate_key() -> преобразование ключа прошло успешно. Ключ: {valid_key}")
                    self.data.key = valid_key

            except ValueError:
                print(f"Validator -> validate_key() -> ошибка при валидации ключа. Ключ: {key}")
                self.data.key = 0
        elif self.data.encryption_type == Encryption_type.VIGENER:
            self.data.key = key.lower() # TODO доделать валидацию

            if self._check_alphabet_set(key, self.data.current_alphabet):
                self.data.key = key
            else:
                return "key"

        elif self.data.encryption_type == Encryption_type.AUTORS:
            if self._check_alphabet_set(key, self.data.current_alphabet):
                self.data.key = key
            else:
                return "key"

    def _check_alphabet_set(self, text, allowed_chars):
        """ проверяет текст на наличие запрещенных символов
         :return: возвращает false при наличии запрещенных символов, true при их отсутствии"""
        # TODO:   добавить вывод ошибки на табло с информацией при нахождении неправильного символа
        return set(text).issubset(set(allowed_chars))