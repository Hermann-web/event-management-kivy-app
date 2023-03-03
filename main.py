# main.py
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from list_screen import ListScreen
from login_screen import LoginScreen

class UserListApp(MDApp):
    def build(self):
        # Create a screen manager
        sm = ScreenManager()

        # Add the screens to the manager and set the initial screen
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(ListScreen(name='list_screen'))
        sm.current = 'login_screen'

        return sm

if __name__ == '__main__':
    UserListApp().run()
