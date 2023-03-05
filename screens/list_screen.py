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
from db.crud_functions import get_clients, filter_clients



from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
#from screens.recycler_view import *

from kivy.uix.boxlayout import BoxLayout

from config import logging
import threading
#------------------------------------

class MessageBox(Popup):
    def __init__(self, **kwargs):
        kwargs_ = kwargs.copy()
        del kwargs['id_client']
        del kwargs['disp_data']
        del kwargs['screen_root']
        super(MessageBox, self).__init__(**kwargs)
        self.id_client = kwargs_['id_client']
        self.screen_root = kwargs_['screen_root']
        self.ids.disp_user_data.text = kwargs_['disp_data']

    def popup_dismiss(self):
        self.dismiss()
    def go_to_user_events(self):
        self.screen_root.view_events(self.id_client)
        self.dismiss()

    
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """
    selected_value = StringProperty('')
    # btn_info = ListProperty(['Button 0 Text', 'Button 1 Text', 'Button 2 Text'])

class MySelectableRows(BoxLayout, RecycleDataViewBehavior, Button):
    """ Add selection support to the Label """
    index = None
    
    a    = StringProperty('')
    b    = StringProperty('')
    c     = StringProperty('')
    d    = StringProperty('')
    e     = StringProperty('')

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(MySelectableRows, self).refresh_view_attrs(rv, index, data)
    
    def view_events_by_user(self, id_client):
        self.root = self.parent.parent.parent.parent
        self.root.view_events(id_client)

    def on_press(self):
        self.is_header = self.idx ==''
        logging.debug(f"self.idx = {self.idx} self.is_header = {self.is_header}")
        if self.is_header: return
        logging.debug("just pressed it")

        # get data on user
        self.root = self.parent.parent.parent.parent
        idx, text, disp = self.idx, self.text, self.disp
        users = self.root.ids.my_list.data
        the_row = list(filter(lambda x: x['idx']==idx, users))[0]
        logging.debug(f"user data: {the_row}")

        # set id_client 
        self.id_client = idx

        # # handle click to go to anotherpage from the msgbox
        # logging.info("handle click to go to anotherpage from the msgbox")
        # fct_view_events_by_user = lambda id_client=self.id_client: self.view_events_by_user(id_client)
        # self.root.manager.register_data('screen_list_msgbox_view_events_by_user', fct_view_events_by_user)

        # add value so the msgbox can read
        logging.info("create str to print on popup")
        self.selected_value = f'Selected: id = {idx} text = {disp}'
        # logging.info("save the str into register data")
        # self.root.manager.register_data("message_box_text", self.selected_value)

        '''rv = self.parent.parent
        my_list_data = rv.data'''
        
    def on_release(self):
        if self.is_header: return
        screen_root = self.parent.parent.parent.parent
        msgbox = MessageBox(id_client=self.id_client, 
                            disp_data=self.selected_value, 
                            screen_root=screen_root,
                            #content = Label(text=disp_data), #iwould need to add buttons on it and group all in a layout
                            title = "rrr")
        msgbox.open()
##-------------------------


Builder.load_file(__file__[:-2]+"kv")


class ListScreen(Screen):
    def __init__(self, **kwargs):
        super(ListScreen, self).__init__(**kwargs)
        self.screen_name = kwargs["name"]
        self._trigger_search = None
    
    def on_pre_enter(self, *args):
        #self.ids.user_list.clear_widgets()
        '''users = [{'firstname': 'John', 'surname': 'Doe', 'cin': '1234567890', 'role': 'Manager', 'firm': 'ACME Inc.'},
                 {'firstname': 'Jane', 'surname': 'Doe', 'cin': '0987654321', 'role': 'Employee', 'firm': 'ACME Inc.'},
                 {'firstname': 'Bob', 'surname': 'Smith', 'cin': '1357908642', 'role': 'Employee', 'firm': 'XYZ Corp'}]'''
        
        # call the get_clients function to retrieve a list of client dictionaries
        users = get_clients()
        '''for user in users:
            user_item = TwoLineListItem(text=user['firstname'] + " " + user['surname'],
                                        secondary_text=f"[color=0000ff][b]CIN:[/b] {user['cin']}\n"
                                                       f"[color=00ff00][b]Firm:[/b][/color] {user['firm']}\n"
                                                       f"[color=ff0000][b]Role:[/b][/color] {user['role']}",
                                        on_press=lambda e,client_id=user["index"]: self.view_events(client_id),
                                        #markup=True
                                        )
        '''
        self.add_users_for_recycler_view(users)

        

    def add_users_for_recycler_view(self, users):
        print("got",[elt['index'] for elt in users])
        h = {'idx':'', 'disp': '', 'a':'firstname', 'b':'surname', 'c':'cin', 'd':'role', 'e':'firm'}
        self.ids.my_list.data = [h] + [{'idx':user["index"], 'disp': self.user_to_str(user), 'a':user['firstname'], 'b':user['surname'], 'c':user['cin'], 'd':user['role'], 'e':user['firm']} for user in users] #[{'text': user['firstname'] + " " + user['surname']} for user in users]
        self.add_pointer_focus()
        self.ids.nb_results.text = f"{len(users)} results"

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
    
    def search_clients(self):
        user_input = self.ids.search_input.text
        logging.debug(f"user filtering from input: {user_input}")
        results = filter_clients(user_input)
        logging.debug(f"nb user filtered: {len(results)}")
        logging.debug(f"user filtered: {[elt['index'] for elt in results]}")
        self.add_users_for_recycler_view(results)
    
    def add_pointer_focus(self):
        self.ids.search_input.focus = True

    def reset_search_timer(self):
        if self._trigger_search:
            self._trigger_search.cancel()
        self._trigger_search = threading.Timer(2.0, self.search_clients)
        self._trigger_search.start()
