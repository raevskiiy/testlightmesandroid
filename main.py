# main.py
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import requests

SERVER_URL = "http://10.0.2.2:8000"  # для эмулятора Android (localhost пробрасывается так)

class MessengerUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.username = TextInput(hint_text="Имя пользователя")
        self.password = TextInput(hint_text="Пароль", password=True)
        self.receiver = TextInput(hint_text="Кому отправить")
        self.message = TextInput(hint_text="Сообщение")

        self.output = Label(text="")

        self.add_widget(self.username)
        self.add_widget(self.password)
        self.add_widget(self.receiver)
        self.add_widget(self.message)

        self.add_widget(Button(text="Регистрация", on_press=self.register))
        self.add_widget(Button(text="Отправить", on_press=self.send_message))
        self.add_widget(Button(text="Получить", on_press=self.get_messages))
        self.add_widget(self.output)

    def register(self, instance):
        data = {"username": self.username.text, "password": self.password.text}
        r = requests.post(f"{SERVER_URL}/register", json=data)
        self.output.text = str(r.json())

    def send_message(self, instance):
        data = {
            "sender": self.username.text,
            "receiver": self.receiver.text,
            "text": self.message.text
        }
        r = requests.post(f"{SERVER_URL}/send", json=data)
        self.output.text = str(r.json())

    def get_messages(self, instance):
        r = requests.get(f"{SERVER_URL}/messages/{self.username.text}")
        self.output.text = str(r.json())

class MessengerApp(App):
    def build(self):
        return MessengerUI()

if __name__ == "__main__":
    MessengerApp().run()
