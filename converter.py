import data
from data import Mode, Encryption_type
import random
import hashlib

class Converter:
    def __init__(self, data):
        self.data = data

    def convert(self, line, key):
        # было:
            # if self.data.mode == Mode.ENCRYPTION:
            #     self.encrypt(line, key)
            # elif self.data.mode == Mode.DECRYPTION:
            #     self.decrypt(line, key)
        # стало:
        try:
            if self.data.mode == Mode.ENCRYPTION:
                self.encrypt(line, key)
            elif self.data.mode == Mode.DECRYPTION:
                self.decrypt(line, key)

            self.data.info_text = "Операция выполнена успешно"

        except ValueError as ex:
            self.data.result = ""
            self.data.info_text = f"Ошибка: {str(ex)}"

    def generate_rubish_symbols(self, number_of_rubish_symbols):
        '''
        Возвращает мусорные символы
        :param number_of_rubish_symbols: количество возвращаемых символов
        :return: rubish_symbols
        '''
        rubish_bin_numbers = ""
        for i in range(number_of_rubish_symbols):
            #   было:
                # random_number = random.randint(0, self.data.len_bin_number - 1)
            #   стало:
            random_number = random.randint( 0, 2 ** self.data.len_bin_number - 1 )

            rubish_bin_numbers += f"{random_number:0{self.data.len_bin_number}b}"
        return rubish_bin_numbers

    def encrypt(self, text, key):
        indexes = []
        new_indexes = []
        code = ""
        text_length = len(text)

        if self.data.encryption_type == self.data.encryption_type.CAESAR:
            for number in text:
                index = self.data.current_alphabet.index(number)
                indexes.append(index)

            for index in indexes:
                new_index = (index + key) % len(self.data.current_alphabet)
                new_indexes.append(new_index)

            for new_index in new_indexes:
                code += self.data.current_alphabet[new_index]

            print(f"Converter -> convert() -> Code: {code}")
            self.data.result = code

        elif self.data.encryption_type == self.data.encryption_type.VIGENER:
            # получение индексов исходного текста
            list_indexes_text = []
            for number in text:
                index = self.data.current_alphabet.index(number)
                list_indexes_text.append(index)

            # получение потока ключей
            list_keys = []
            for i in range(text_length):
                list_keys.append(key[i % len(key)])


            # получение потока индексов ключей
            list_indexes_keys = []
            for number in list_keys:
                list_indexes_keys.append(self.data.current_alphabet.index(number))

            # получение индексов кода
            indexes_code = []
            for i in range(text_length):
                indexes_code.append(list_indexes_text[i] + list_indexes_keys[i])

            # приводим значение индексов к допустимому диапазону
            normal_indexes_code = []
            for index in indexes_code:
                normal_indexes_code.append(index % len(self.data.current_alphabet))

            # получаем код
            code = ""
            for index in normal_indexes_code:
                code += self.data.current_alphabet[index]
            self.data.result = code

        elif self.data.encryption_type == self.data.encryption_type.AUTORS:

            # получаем индексы текста
            list_indexes_text = []
            for number in text:
                index = self.data.current_alphabet.index(number)
                list_indexes_text.append(index)

            # получаем поток символов ключа
            list_keys = []
            for i in range(text_length):
                list_keys.append(key[i % len(key)])

            # получение потока индексов ключа
            list_indexes_keys = []
            for number in list_keys:
                list_indexes_keys.append(self.data.current_alphabet.index(number))

            # получаем побитовый xor для каждых i-их элементов из списков list_indexes_text и list_indexes_keys
            list_xor = []
            for i in range(len(list_indexes_text)):
                xor = list_indexes_text[i]^list_indexes_keys[i]
                list_xor.append(f"{xor:0{self.data.len_bin_number}b}")

            # получаем xor
            # xor_indexes = []
            # for element in list_xor:
            #     xor_indexes.append(int(element[2:], 2))

            # # приводим к допустимому диапазону индексов алфавита
            # correct_xor_indexes = []
            # for element in xor_indexes:
            #     correct_xor_indexes.append(element % len(self.data.current_alphabet))

            # # преобразуем индексы в символы алфавита
            # list_symbols_code = []
            # for index in correct_xor_indexes:
            #     list_symbols_code.append(self.data.current_alphabet[index])

            # добавляем мусорные символы
            #   было:
                # # находим X(сумма индексов ключа)
                # x = sum(list_indexes_keys[0:len(key)])
                #
                # # находим Y` по формуле Y` = (X` % (len(key) + len(alphabet))) / len(key) (количество мусорных символов)
                # hash_value = hashlib.sha256(key.encode()).digest()
            #   стало:
            hash_value = hashlib.sha256(key.encode()).digest()
            y = (hash_value[0] % self.data.range_y) + 1



            # добавление мусорных символов в код
            code = ""
            #   было:
                # count = 0
                # for number in list_xor:
                #     if count == len(key):
                #         code += self.generate_rubish_symbols(y)
                #         count = 0
                #     else:
                #         count += 1
                #     code += number
            #   стало:
            count = 0
            for number in list_xor:
                code += number
                count += 1
                if count == len(key):
                    code += self.generate_rubish_symbols(y)
                    count = 0


            code = f"{self.generate_rubish_symbols(y)}{code}"
            code += self.generate_rubish_symbols(y)
            self.data.result = code

    def decrypt(self, code, key):
        indexes = []
        new_indexes = []
        text = ""
        if self.data.encryption_type == self.data.encryption_type.CAESAR:

            for i in code:
                index = self.data.current_alphabet.index(i)
                indexes.append(index)

            for index in indexes:
                new_index = (index - key) % len(self.data.current_alphabet)
                new_indexes.append(new_index)

            for new_index in new_indexes:
                text += self.data.current_alphabet[new_index]
                print(f"Converter -> convert() -> Code: {text}")
                self.data.result = text


        elif self.data.encryption_type == self.data.encryption_type.VIGENER:
            # получение индексов исходного кода
            list_indexes_code = []
            for i in code:
                index = self.data.current_alphabet.index(i)
                list_indexes_code.append(index)

            # получение потока ключей
            list_keys = []
            for i in range(len(code)):
                list_keys.append(key[i % len(key)])

            # получение потока индексов ключей
            list_indexes_keys = []
            for i in list_keys:
                list_indexes_keys.append(self.data.current_alphabet.index(i))

            # получение индексов текста
            indexes_text = []
            for i in range(len(code)):
                indexes_text.append(list_indexes_code[i] - list_indexes_keys[i])

            # приводим значение индексов к допустимому диапазону
            normal_indexes_code = []
            for index in indexes_text:
                normal_indexes_code.append(index % len(self.data.current_alphabet))

            # получаем текст
            text = ""
            for index in normal_indexes_code:
                text += self.data.current_alphabet[index]
            self.data.result = text


        elif self.data.encryption_type == self.data.encryption_type.AUTORS:
            # удаляем мусорные символы

            # получение индексов ключа
            list_indexes_key = []
            for symbol in key:
                list_indexes_key.append(self.data.current_alphabet.index(symbol))

            #   было:
                # # находим X(сумма индексов ключа)
                # x = sum(list_indexes_keys[0:len(key)])
                #
                # # находим Y` по формуле Y` = (X` % (len(key) + len(alphabet))) / len(key) (количество мусорных символов)
                # hash_value = hashlib.sha256(key.encode()).digest()
            #   стало:
            hash_value = hashlib.sha256(key.encode()).digest()
            y = (hash_value[0] % 5) + 1

            # удаляем первую группу мусорных символов и последюю
            number_rubish_symbols_in_bin_group = y * self.data.len_bin_number
            code_without_first_and_end_rubish_symbols = f"{code[number_rubish_symbols_in_bin_group:-number_rubish_symbols_in_bin_group]}"

            # получаем код без мусорных символов
            clear_code = ""
            counter_text_symbols = 0
            counter_rubish_symbols = 0

            #   было:
                # for i in range(len(code_without_first_and_end_rubish_symbols) // self.data.len_bin_number): # range(длина закодированного слова в символах)
                #     if counter_text_symbols < len(key): # проверяем на то что символ входит в группу символов текста
                #         clear_code += code_without_first_and_end_rubish_symbols[i*self.data.len_bin_number:(i+1) * self.data.len_bin_number] # добавляем в clear_code текущий символ
                #         counter_text_symbols += 1
                #     elif counter_rubish_symbols < y:
                #         counter_rubish_symbols += 1
                #     else:
                #         clear_code += code_without_first_and_end_rubish_symbols[i*self.data.len_bin_number:(i+1) * self.data.len_bin_number] # добавляем в clear_code текущий символ
                #         counter_rubish_symbols = 0
                #         counter_text_symbols = 1
            #   стало:
            symbols = []
            for i in range( 0, len(code_without_first_and_end_rubish_symbols), self.data.len_bin_number ):
                symbols.append( code_without_first_and_end_rubish_symbols[ i:i + self.data.len_bin_number ])

            clear_symbols = []
            position = 0
            while position < len(symbols):
                clear_symbols.extend( symbols[position:position + len(key)] )
                position += len(key)
                position += y

            clear_code = "".join(clear_symbols)   # конец стало


            text_length = len(clear_code) // self.data.len_bin_number

            # получаем поток символов ключа
            list_keys = []
            for i in range(text_length):
                list_keys.append(key[i % len(key)])

            # получение потока индексов ключа
            list_indexes_keys = []
            for number in list_keys:
                list_indexes_keys.append(self.data.current_alphabet.index(number))

            # получаем побитовый xor для каждых i-их элементов из списков list_indexes_code и list_indexes_keys
            list_xor = []
            for i in range(text_length):
                xor = int(clear_code[self.data.len_bin_number * i:self.data.len_bin_number * (1 + i)], 2)^list_indexes_keys[i]
                list_xor.append(xor)

            text = ""
            for index in list_xor:
                #   было:
                    # text += self.data.current_alphabet[index]
                #   стало:
                if index >= len(self.data.current_alphabet):
                    raise ValueError(
                        f"Получен недопустимый индекс {index}"
                    )
                text += self.data.current_alphabet[index]

            self.data.result = text