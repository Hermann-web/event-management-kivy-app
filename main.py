# main.py
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from list_screen import ListScreen
from login_screen import LoginScreen
from list_user_events import ListUserEventsScreen
from config import screen_login_str, screen_list_participants_str, screen_list_user_events_str

class RootScreenManager(ScreenManager):
    def switch_screen(self, screen_name, **kwargs):
        if screen_name == screen_login_str:
            direction = 'right'
        elif screen_name == screen_list_participants_str:
            direction = 'left'
        else:
            direction = 'down'
        self.transition = SlideTransition(direction=direction)
        self.data = kwargs
        self.current = screen_name
    
    def to_login_screen(self):
        self.switch_screen(screen_login_str)
    def to_users_list_screen(self):
        self.switch_screen(screen_list_participants_str)
    def to_user_events_list_screen(self, client_id):
        self.switch_screen(screen_list_user_events_str, client_id=client_id)
    def to_events_screen(self):
        self.switch_screen(screen_list_events_str)

'''class CustomSlideTransition(SlideTransition):
    def get_direction(self, screen_manager, screen1, screen2):
        print(screen_manager.current, screen1, screen2)
        if screen_manager.current == screen_login_str:
            print("going num again !")
            return 'right'
        return 'left'
        
class RootScreenManager(ScreenManager):
    def switch_screen(self, screen_name):
        self.current = screen_name
'''

class UserListApp(MDApp):
    def build(self):
        # Create a screen manager
        self.theme_cls.theme_style = "Dark"
        # sm = RootScreenManager(transition=CustomSlideTransition())
        # sm = ScreenManager()
        # Add the screens to the manager and set the initial screen
        sm = RootScreenManager()

        sm.add_widget(LoginScreen(name=screen_login_str))
        sm.add_widget(ListScreen(name=screen_list_participants_str))
        sm.add_widget(ListUserEventsScreen(name=screen_list_user_events_str))
        sm.current = screen_login_str
        self.sm = sm
        return sm
    
    def to_login_screen(self):
        self.sm.switch_screen(screen_login_str)
    def to_users_list_screen(self):
        self.sm.switch_screen(screen_list_participants_str)
    def to_user_events_list_screen(self,client_id):
        self.sm.to_user_events_list_screen(client_id)
    def to_events_screen(self):
        self.sm.switch_screen(screen_list_events_str)



if __name__ == '__main__':
    UserListApp().run()



