from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList, TwoLineListItem, ImageLeftWidget
from kivy.lang import Builder

Builder.load_file('list_screen.kv')


class ListScreen(Screen):
    def __init__(self, **kwargs):
        super(ListScreen, self).__init__(**kwargs)
    
    def on_pre_enter(self, *args):
        users = [{'firstname': 'John', 'surname': 'Doe', 'cin': '1234567890', 'role': 'Manager', 'firm': 'ACME Inc.'},
                 {'firstname': 'Jane', 'surname': 'Doe', 'cin': '0987654321', 'role': 'Employee', 'firm': 'ACME Inc.'},
                 {'firstname': 'Bob', 'surname': 'Smith', 'cin': '1357908642', 'role': 'Employee', 'firm': 'XYZ Corp'}]
        for user in users:
            user_item = TwoLineListItem(text=user['firstname'] + " " + user['surname'],
                                        secondary_text=f"[b]CIN:[/b] {user['cin']}\n"
                                                       f"[color=00ff00][b]Firm:[/b][/color] {user['firm']}\n"
                                                       f"[color=ff0000][b]Role:[/b][/color] {user['role']}",
                                        #markup=True
                                        )
            self.ids.user_list.add_widget(user_item)
