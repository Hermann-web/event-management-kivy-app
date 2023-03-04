## login_screen.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from config import screen_login_str, screen_list_participants_str
from kivy.lang import Builder

Builder.load_file('login_screen.kv')

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    username_field = ObjectProperty(None)
    password_field = ObjectProperty(None)

    def login(self, username, password):
        # TODO: Add login logic here

        # If login is successful, switch to ListScreen
        self.manager.to_users_list_screen()