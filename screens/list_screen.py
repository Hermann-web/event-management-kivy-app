from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, StringProperty, ObjectProperty

## list_screen.py
import os.path
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList, TwoLineListItem, ImageLeftWidget
from kivy.lang import Builder
#from db.db_json.clients_handler import get_clients
from db.crud_functions import get_clients



from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
#from screens.recycler_view import *



#------------------------------------
class MessageBox(Popup):
    def popup_dismiss(self):
        self.dismiss()
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """
    selected_value = StringProperty('')
    # btn_info = ListProperty(['Button 0 Text', 'Button 1 Text', 'Button 2 Text'])
class SelectableButton(RecycleDataViewBehavior, Button):
    """ Add selection support to the Label """
    index = None
    
    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)
    def on_press(self):
        self.root = self.parent.parent.parent.parent
        self.parent.selected_value = 'Selected: {}'.format(self.text)
        #self.root.ids.label_message_box.text = self.parent.selected_value
        self.root.manager.register_data("message_box_text", self.parent.selected_value)
    
    def on_release(self):
        MessageBox().open()
        # self.root = self.parent.parent.parent.parent
        # selected_value = self.root.selectable_box_layout.selected_value
        # print(selected_value)

##-------------------------


Builder.load_file(__file__[:-2]+"kv")


class ListScreen(Screen):
    def __init__(self, **kwargs):
        super(ListScreen, self).__init__(**kwargs)
        self.screen_name = kwargs["name"]
        self.ids.my_list.data = [{'text': "Button " + str(x), 'id': str(x)} for x in range(3)]
        # self.selectable_box_layout = self.ids.my_list.rv_layout

    def on_pre_enter(self, *args):
        #self.ids.user_list.clear_widgets()
        '''users = [{'firstname': 'John', 'surname': 'Doe', 'cin': '1234567890', 'role': 'Manager', 'firm': 'ACME Inc.'},
                 {'firstname': 'Jane', 'surname': 'Doe', 'cin': '0987654321', 'role': 'Employee', 'firm': 'ACME Inc.'},
                 {'firstname': 'Bob', 'surname': 'Smith', 'cin': '1357908642', 'role': 'Employee', 'firm': 'XYZ Corp'}]'''
        
        # call the get_clients function to retrieve a list of client dictionaries
        self.users = get_clients()
        '''for user in users:
            user_item = TwoLineListItem(text=user['firstname'] + " " + user['surname'],
                                        secondary_text=f"[color=0000ff][b]CIN:[/b] {user['cin']}\n"
                                                       f"[color=00ff00][b]Firm:[/b][/color] {user['firm']}\n"
                                                       f"[color=ff0000][b]Role:[/b][/color] {user['role']}",
                                        on_press=lambda e,client_id=user["index"]: self.view_events(client_id),
                                        #markup=True

                                        )
        '''
        self.ids.my_list.data = [{'text': self.user_to_str(user)} for user in self.users] #[{'text': user['firstname'] + " " + user['surname']} for user in users]

    def user_to_str(self, user):
        return f"{user['firstname']} {user['surname']} {user['cin']} \n{user['role']}, {user['firm']}"
    
    def to_login_screen_(self):
        self.manager.to_login_screen(self.screen_name)

    def to_events_screen_(self):
        self.manager.to_events_screen(self.screen_name)
    
    def to_user_events_list_screen_(self, client_id):
        self.manager.to_user_events_list_screen(self.screen_name, client_id=client_id)

    def view_events(self, client_id):
        # Here, you can retrieve the events for the given client_id and display them in the user_events screen.
        # You can use the id_event to retrieve the event information from the database.
        print("client_id = ",client_id)
        self.to_user_events_list_screen_(client_id=client_id)