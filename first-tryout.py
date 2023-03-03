#!/usr/bin/env python
# -*- coding: utf-8 -*-
# source
# https://stackoverflow.com/questions/67074497/how-to-change-current-screen-in-kivy

__author__      = "Hermann Agossou"


from kivymd.app import MDApp
from kivymd.uix.list import MDList, TwoLineListItem, ImageLeftWidget
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivymd.uix.button import MDFloatingActionButton, MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

screen_helper = """
ScreenManager:
    LoginScreen:
        id: login_scr
    ListScreen:
        id: list_scr

<LoginScreen>:
    name: 'login'
    MDTextField:
        id: email
        hint_text: "Email"
        pos_hint: {'center_x':0.5, 'center_y':0.6}
    MDTextField:
        id: password
        hint_text: "Password"
        password: True
        pos_hint: {'center_x':0.5, 'center_y':0.5}
    MDRectangleFlatButton:
        text: 'Login'
        id: login
        pos_hint: {'center_x':0.25, 'center_y':0.4}
        on_press: app.login()

<ListScreen>:
    name: 'myList'
    ScrollView:
        MDList:
            id: user_list
            TwoLineListItem:
                text: "John Smith"
                secondary_text: "CIN: 1234567890"
            TwoLineListItem:
                text: "John Smith"
                secondary_text: "CIN: 0987654321"
    MDFloatingActionButton:
        icon: 'plus'
        pos_hint: {'center_x':0.9, 'center_y':0.05}
        on_press: root.manager.current = 'assignment'
    MDFloatingActionButton:
        icon: 'theme-light-dark'
        pos_hint: {'center_x':0.1, 'center_y':0.05}
        on_press: app.show_theme_picker()
    MDRectangleFlatButton
        id: sortButton
        pos_hint: {'center_x':0.5, 'center_y':0.05}
        text: "Sorted by: Deadline"
        on_press: app.sort()
"""


class LoginScreen(Screen):
    pass


class ListScreen(Screen):
    def on_enter(self):
        # Clear any existing items in the list
        self.ids.user_list.clear_widgets()
        
        # List of user dictionaries
        users = [
            {'firstname': 'John', 'surname': 'Doe', 'cin': '1234567890', 'firm': 'ACME Inc.', 'role': 'Manager'},
            {'firstname': 'Jane', 'surname': 'Smith', 'cin': '0987654321', 'firm': 'Globex Corp.', 'role': 'Employee'},
            # Add more users here...
        ]
        
        # Create an MDListItem for each user and add it to the list
        for user in users:
            '''item = TwoLineListItem(
                text=f"[b]Firstname:[/b] {user['firstname']}\n[b]Surname:[/b] {user['surname']}",
                secondary_text=f"[b]CIN:[/b] {user['cin']}    [b]Role:[/b] {user['role']}    [b]Firm:[/b] {user['firm']}",
                #markup=True
            )
            
            self.ids.user_list.add_widget(item)'''

            user_item = TwoLineListItem(text=user['firstname'] + " " + user['surname'],
                                        secondary_text=f"[b]CIN:[/b] {user['cin']}\n"
                                                       f"[color=00ff00][b]Firm:[/b][/color] {user['firm']}\n"
                                                       f"[color=ff0000][b]Role:[/b][/color] {user['role']}",
                                        )
            # item.add_widget(ImageLeftWidget(source="https://pic.onlinewebfonts.com/svg/img_24787.png"))
            self.ids.user_list.add_widget(user_item)


class AssignmentTracker(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        screen = Builder.load_string(screen_helper)
        return screen

    def login(self):
        print(self.root.current_screen)
        self.root.current = 'myList'
    
    def sort(self):
        pass
        

Window.size = (350, 700)
AssignmentTracker().run()