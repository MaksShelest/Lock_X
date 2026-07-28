from enum import Enum

class Data:
    def __init__(self, key):
        self.alphabet = [
            # English lowercase
            'a','b','c','d','e','f','g','h','i','j','k','l','m',
            'n','o','p','q','r','s','t','u','v','w','x','y','z',

            # digits
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',

            # English uppercase
            'A','B','C','D','E','F','G','H','I','J','K','L','M',
            'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',

            # Russian-specific symbols
            #   было:
                # '№', " ", "!"
            #   стало:
            '№', ' ', '!', '\n', '—',

            # Russian lowercase
            'а','б','в','г','д','е','ё','ж','з','и','й','к','л','м',
            'н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ',
            'ы','ь','э','ю','я',

            # special symbols (common keyboard)
            '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+',
            '[', '{', ']', '}', '\\', '|', ';', ':', "'", '"', ',', '<', '.', '>', '/', '?',

            # Russian uppercase
            'А','Б','В','Г','Д','Е','Ё','Ж','З','И','Й','К','Л','М',
            'Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Ъ',
            'Ы','Ь','Э','Ю','Я',

        ]

        # text:  hello
        #  key:  gdegd
        # code:  n

        self.alphabet_eng = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '0']
                         # "['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '0']
        self.alphabet_rus = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]
        self.current_alphabet = self.alphabet
        self.key = key
        self.text = ""
        self.code = ""
        self.result = ""
        self.len_bin_number = 8
        self.range_y = 5  # максимальная длина одной группы мусорных символов (от 1 до range_y)
        self.base_info_text = "Информация"
        self.info_text = self.base_info_text
        self.mode = Mode.ENCRYPTION
        self.encryption_type = Encryption_type.AUTORS
        self.operations_list = []

    def set_mode(self, instance, value):
        if value == Mode.ENCRYPTION.value:
            self.mode = Mode.ENCRYPTION
            print(f"Data -> set_mode() -> смена значения mode: {value}")
        elif value == Mode.DECRYPTION.value:
            self.mode = Mode.DECRYPTION
            print(f"Data -> set_mode() -> смена значения mode: {value}")
        else:
            print(f"Data -> set_mode() -> ошибка: несуществующий mode: {value}")

    def set_encryption_type(self, instance, value):
        if value == Encryption_type.CAESAR.value:
            self.encryption_type = Encryption_type.CAESAR
            print(f"Data -> set_encryption_type() -> смена значения encryption_type: {value}")
        elif value == Encryption_type.VIGENER.value:
            self.encryption_type = Encryption_type.VIGENER
            print(f"Data -> set_encryption_type() -> смена значения encryption_type: {value}")
        elif value == Encryption_type.AUTORS.value:
            self.encryption_type = Encryption_type.AUTORS
            print(f"Data -> set_encryption_type() -> смена значения encryption_type: {value}")
        else:
            print(f"Data -> set_encryption_type() -> ошибка: несуществующий encryption_type: {value}")

class Language(Enum):
    ENG = "ENG"
    RU = "RU"

class Encryption_type(Enum):
    CAESAR = "CAESAR"
    VIGENER = "VIGENER"
    AUTORS = "AUTORS"

class Mode(Enum):
    ENCRYPTION = "ENCRYPTION"
    DECRYPTION = "DECRYPTION"