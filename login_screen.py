# login_screen.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('login_screen.kv')

class LoginScreen(Screen):
    username_field = ObjectProperty(None)
    password_field = ObjectProperty(None)

    def login(self, username, password):
        # TODO: Add login logic here

        # If login is successful, switch to ListScreen
        self.manager.current = 'list_screen'
