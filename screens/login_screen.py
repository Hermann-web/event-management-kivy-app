## login_screen.py
import os.path
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from utils import catch_exceptions

Builder.load_file(__file__[:-2]+"kv")

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.screen_name = kwargs["name"]

    username_field = ObjectProperty(None)
    password_field = ObjectProperty(None)

    @catch_exceptions
    def login(self, username, password):
        # TODO: Add login logic here

        # If login is successful, switch to ListScreen
        self.manager.to_users_list_screen(self.screen_name)