# main.py
from config import logging
import traceback 

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from screens.list_screen import ListScreen
from screens.login_screen import LoginScreen
from screens.list_user_events import ListUserEventsScreen
from config import (
    screen_login_str, screen_list_participants_str, 
    screen_list_user_events_str, screen_list_events_str
)
from config import DEBUG
from utils import log_exception

# for pyinstaller #to make sure the graphic backend is initialized properly
#import kivy_deps
#kivy_deps.angle_backend.ensure_surface_initialized()

class RootScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(RootScreenManager, self).__init__(**kwargs)
        self._app_data_ = {}

    def switch_screen(self, screen_name, current, **kwargs):
        try:
            if current == screen_login_str:
                direction = 'up'
            elif screen_name == screen_login_str:
                direction = 'down'
            
            elif current == screen_list_user_events_str:
                direction = 'down'
            elif screen_name == screen_list_user_events_str:
                direction = 'up'
            
            elif current == screen_list_participants_str:
                if screen_name == screen_list_events_str:
                    direction = 'left'
                else:
                    direction = ''
            elif current == screen_list_events_str:
                if screen_name == screen_list_participants_str:
                    direction = 'right'
                else:
                    direction = ''
            else:
                direction = ''
            self.transition = SlideTransition(direction=direction)
            self.data = kwargs
            self.current = screen_name
        except Exception as e:
            self.display_error_message(e, f"switching screens from {current} to {screen_name}")

    def to_login_screen(self, current):
        try:
            self.switch_screen(screen_login_str, current=current)
        except Exception as e:
            self.display_error_message(e, "switching to login screen")

    def to_users_list_screen(self, current):
        try:
            self.switch_screen(screen_list_participants_str, current=current)
        except Exception as e:
            self.display_error_message(e, "switching to user list screen")

    def to_user_events_list_screen(self, current, client_id):
        try:
            self.switch_screen(screen_list_user_events_str, current=current, client_id=client_id)
        except Exception as e:
            self.display_error_message(e, "switching to user events screen")

    def to_events_screen(self, current):
        try:
            self.switch_screen(screen_list_events_str, current=current)
        except Exception as e:
            self.display_error_message(e, "switching to events screen")
    
    def show_popup(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(400, 400))
        popup.open()

    def display_error_message(self, err, action):
        error_message = "An error occurred. Please try again later."
        if DEBUG: error_message += f"\n--> {action}\n err:{err}"
        self.show_popup(error_message)
        log_exception(err, action)

    def register_data(self, id, data):
        self._app_data_[id] = data
        logging.debug(f"register id = {id} data = {data}")

    def get_register_data(self, id):
        return self._app_data_[id]


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

    
    def to_login_screen(self, current):
        try:
            self.sm.to_login_screen(current)
        except Exception as e:
            logging.error(f"An error occurred while switching to login screen: {e}")
            self.sm.show_popup("An error occurred. Please try again later.")

    def to_users_list_screen(self, current):
        try:
            self.sm.to_users_list_screen(current)
        except Exception as e:
            logging.error(f"An error occurred while switching to users list screen: {e}")
            self.sm.show_popup("An error occurred. Please try again later.")

    def to_user_events_list_screen(self, current, client_id):
        try:
            self.sm.to_user_events_list_screen(current, client_id)
        except Exception as e:
            logging.error(f"An error occurred while switching to user events list screen: {e}")
            self.sm.show_popup("An error occurred. Please try again later.")

    def to_events_screen(self, current):
        try:
            self.sm.to_events_screen(current)
        except Exception as e:
            logging.error(f"An error occurred while switching to events list screen: {e}")
            self.sm.show_popup("An error occurred. Please try again later.")



if __name__ == '__main__':
    app = UserListApp()
    app.run()
    '''
    from kivy.resources import resource_add_path, resource_find
    try:
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))
        app = UserListApp()
        app.run()
    except Exception as e:
        print(e)
        input("Press enter.")'''