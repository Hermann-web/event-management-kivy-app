# main.py
from config import logging

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from list_screen import ListScreen
from login_screen import LoginScreen
from list_user_events import ListUserEventsScreen
from config import (
    screen_login_str, screen_list_participants_str, 
    screen_list_user_events_str, screen_list_events_str
)
from config import DEBUG

class RootScreenManager(ScreenManager):
    def switch_screen(self, screen_name, **kwargs):
        try:
            if screen_name == screen_login_str:
                direction = 'right'
            elif screen_name == screen_list_participants_str:
                direction = 'left'
            else:
                direction = 'down'
            self.transition = SlideTransition(direction=direction)
            self.data = kwargs
            self.current = screen_name
        except Exception as e:
            self.display_error_message(e, "switching screens")

    def to_login_screen(self):
        try:
            self.switch_screen(screen_login_str)
        except Exception as e:
            self.display_error_message(e, "switching to login screen")

    def to_users_list_screen(self):
        try:
            self.switch_screen(screen_list_participants_str)
        except Exception as e:
            self.display_error_message(e, "switching to user list screen")

    def to_user_events_list_screen(self, client_id):
        try:
            self.switch_screen(screen_list_user_events_str, client_id=client_id)
        except Exception as e:
            self.display_error_message(e, "switching to user events screen")

    def to_events_screen(self):
        try:
            self.switch_screen(screen_list_events_str)
        except Exception as e:
            self.display_error_message(e, "switching to events screen")
    
    def show_popup(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(400, 400))
        popup.open()

    def display_error_message(self, err, action):
        detail_ = f"--> {action}\n err:{err}"
        logging.error(detail_)
        error_message = "An error occurred. Please try again later."
        if DEBUG: error_message += "\n" + detail_
        self.show_popup(error_message)


class UserListApp(MDApp):
    def build(self):
        # Create a screen manager
        self.theme_cls.theme_style = "Dark"
        sm = RootScreenManager()
        sm.add_widget(LoginScreen(name=screen_login_str))
        sm.add_widget(ListScreen(name=screen_list_participants_str))
        sm.add_widget(ListUserEventsScreen(name=screen_list_user_events_str))
        sm.current = screen_login_str
        self.sm = sm
        return sm

    
    def to_login_screen(self):
        try:
            self.sm.switch_screen(screen_login_str)
        except Exception as e:
            logging.error(f"An error occurred while switching to login screen: {e}")
            self.sm.show_popup("An error occurred. Please try again later.")

    def to_users_list_screen(self):
        try:
            self.sm.switch_screen(screen_list_participants_str)
        except Exception as e:
            logging.error(f"An error occurred while switching to users list screen: {e}")
            self.sm.show_popup("An error occurred. Please try again later.")

    def to_user_events_list_screen(self, client_id):
        try:
            self.sm.to_user_events_list_screen(client_id)
        except Exception as e:
            logging.error(f"An error occurred while switching to user events list screen: {e}")
            self.sm.show_popup("An error occurred. Please try again later.")

    def to_events_screen(self):
        try:
            self.sm.switch_screen(screen_list_events_str)
        except Exception as e:
            logging.error(f"An error occurred while switching to events list screen: {e}")
            self.sm.show_popup("An error occurred. Please try again later.")

if __name__ == '__main__':
    UserListApp().run()



