import configuration
import json
from kivy.core.clipboard import Clipboard
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime

from validator import Validator
from data import *
from operation import *
from converter import *
# TODO  -  добавил (
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
# TODO  -  )


# TODO  -  добавил (
class MyScreenManager(ScreenManager):
    pass

class ConverterScreen(Screen):
    pass

class HistoryScreen(Screen):
    pass
# TODO  -  )

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = Data(key=0)
        self.validator = Validator(self.data)
        self.converter = Converter(self.data)

    def press_button_convert(self, *args):
        self.converter.convert(key=self.data.key, line=self.data.text)
        self.root.get_screen("converter_screen").ids.textinput_text_output.text = self.data.result
        self.root.get_screen("converter_screen").ids.label_info.text = self.data.info_text

    def button_copy_press(self):
        Clipboard.copy(self.data.result)

    def build(self):
        Builder.load_file('main.kv')
        sm = MyScreenManager()
        sm.add_widget(ConverterScreen())
        sm.add_widget(HistoryScreen())
        return sm

    def on_start(self):
        self.root.get_screen("converter_screen").ids.textinput_text_input.bind(text = self.validator.event_validate_text)
        self.root.get_screen("converter_screen").ids.textinput_key_input.bind(text = self.validator.event_validate_key)
        self.root.get_screen("converter_screen").ids.spinner_mode.bind(text = self.data.set_mode)
        self.root.get_screen("converter_screen").ids.spinner_encryption_type.bind(text=self.data.set_encryption_type)
        # TODO  -  добавил (
        self.load_operations()
        # TODO  -  )
        pass

    # TODO  -  добавил (
    def on_stop(self):  # сохранение файлов json
        with open("operations.json", "w", encoding="utf-8") as file:
            json.dump(self.data.operations_list, file,
                      default=lambda o: (o.isoformat() if hasattr(o, "isoformat") else o.__dict__), ensure_ascii=False,
                      indent=4)

    # TODO  -  )

    def button_paste_press(self):
        self.root.get_screen("converter_screen").ids.textinput_text_input.text = Clipboard.paste()

    # TODO  -  добавил (
    def load_operations(self):  # загружаем операции
        try:
            with open('operations.json', "r", encoding="utf-8") as file:
                raw_data = json.load(file)  # загружаем данные из json в сырую строку
                restored_list = []
            for item in raw_data:
                if "time" in item:
                    item["time"] = datetime.fromisoformat(item["time"])  # перезаписываем переменную в формат времени
                obj = Operation(**item)
                restored_list.append(obj)
            self.data.operations_list = restored_list
            print("операции успешно загружена")

        except (FileNotFoundError, json.JSONDecodeError):
            print("файл отсутствует или поврежден")
            self.data.operations_list = []
    # TODO  -  )

class ValidationApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


if __name__ == "__main__":
    MainApp().run()




