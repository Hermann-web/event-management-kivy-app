
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

from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty

from db.crud_functions import filter_client_choices_from_text_input
from db.crud_functions import set_present_true
from config.config import logging
import threading
from utils import catch_exceptions, log_exception

#Builder.load_file(__file__[:-2]+"kv")
Builder.load_file('.'.join(__file__.split('.')[:-1])+".kv")
#Builder.load_file("./screens/list_user_events.kv")


class AttendanceMessageBox(Popup):
    def __init__(self, **kwargs):
        kwargs_ = kwargs.copy()
        del kwargs['id_main']
        del kwargs['disp_data']
        del kwargs['screen_root']
        super(AttendanceMessageBox, self).__init__(**kwargs)
        self.id_main = kwargs_['id_main']
        self.screen_root = kwargs_['screen_root']
        self.ids.disp_user_data.text = kwargs_['disp_data']

    @catch_exceptions
    def popup_dismiss(self):
        self.dismiss()
    @catch_exceptions
    def admit_attendance(self):
        self.screen_root.admit_attendance(self.id_main)
        self.dismiss()


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """
    selected_value = StringProperty('')
    # btn_info = ListProperty(['Button 0 Text', 'Button 1 Text', 'Button 2 Text'])

class AttendanceMySelectableRows(BoxLayout, RecycleDataViewBehavior, Button):
    """ Add selection support to the Label """
    index = None
    icon_path = ""
    
    a    = StringProperty('')
    b    = StringProperty('')
    c     = BooleanProperty(False)
    d    = StringProperty('')
    e     = StringProperty('')

    @catch_exceptions
    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        #self.icon_path = data['icon_path']
        return super(AttendanceMySelectableRows, self).refresh_view_attrs(rv, index, data)
    
    @catch_exceptions
    def view_events_by_user(self, id_client):
        self.root = self.parent.parent.parent.parent
        self.root.view_events(id_client)

    @catch_exceptions
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
        self.name = f"{the_row['a']} {the_row['b']}"
        logging.debug(f"user data: {the_row}")

        # set id_client 
        self.id_main = idx

        # # handle click to go to anotherpage from the msgbox
        # logging.info("handle click to go to anotherpage from the msgbox")
        # fct_view_events_by_user = lambda id_client=self.id_client: self.view_events_by_user(id_client)
        # self.root.manager.register_data('screen_list_msgbox_view_events_by_user', fct_view_events_by_user)

        # add value so the msgbox can read
        logging.info("create str to print on popup")
        self.selected_value = f'id = {idx}\n{disp}'
        # logging.info("save the str into register data")
        # self.root.manager.register_data("message_box_text", self.selected_value)

        '''rv = self.parent.parent
        my_list_data = rv.data'''
        
    @catch_exceptions
    def on_release(self):
        if self.is_header: return
        screen_root = self.parent.parent.parent.parent
        msgbox = AttendanceMessageBox(id_main=self.id_main, 
                            disp_data=self.selected_value, 
                            screen_root=screen_root,
                            #content = Label(text=disp_data), #iwould need to add buttons on it and group all in a layout
                            title = self.name)
        msgbox.open()
##-------------------------

class ListUserEventsScreen(Screen):
    def __init__(self, **kwargs):
        super(ListUserEventsScreen, self).__init__(**kwargs)
        self.screen_name = kwargs["name"]
        self._trigger_search = None
    @catch_exceptions
    def on_pre_enter(self, *args):
        client_id = self.manager.data.get("client_id")
        event_id = self.manager.data.get("event_id")
        day = self.manager.data.get("day")
        hour = self.manager.data.get("hour")
        logging.debug(f"client_id landed: {client_id}")
        self.filters = {'id_client':client_id, 'id_event':event_id, 'day':day, 'hour':hour}
        self.add_rows_for_recycler_view()

    def row_screen_dict(self, row:dict):
        return {'idx':row["index"], 'disp': self.row_to_str(row), 'a':str(row['id_event']), 'b':str(row['id_client']), 'c':bool(row['is_present']), 'd':str(row['time_presence']), 'e':''}
    @catch_exceptions
    def add_rows_for_recycler_view(self, user_input=None):
        rows = filter_client_choices_from_text_input(filters=self.filters, text_input=user_input)
        logging.debug(f"nb user filtered: {len(rows)}")
        logging.debug(f"rows index: got {[elt['index'] for elt in rows]}")
        h = {'idx':'', 'disp': '', 'a':'id_event', 'b':'id_client', 
             'c':'is_present', 'd':'time_presence', 'e':''}
        self.ids.my_list.data = [h] + [self.row_screen_dict(row) for row in rows] #[{'text': user['firstname'] + " " + user['surname']} for user in users]
        self.add_pointer_focus()
        self.ids.nb_results2.text = f"{len(rows)} results"

    @catch_exceptions
    def row_to_str(self, row):
        text = ""
        for key,val in row.items():
            if key in ["id","index","id_","_id"]: continue
            text+= f"->{key:^15}: {val}\n"
        return text
        #return f"{user['firstname']} {user['surname']} {user['cin']} \n{user['role']}, {user['firm']}"
    
    def to_login_screen_(self):
        self.manager.to_login_screen(self.screen_name)

    def to_events_screen_(self):
        self.manager.to_events_screen(self.screen_name)
    
    def to_user_events_list_screen_(self, client_id):
        self.manager.to_user_events_list_screen(self.screen_name, client_id=client_id)

    @catch_exceptions
    def update_row(self, index, updated_row):
        for i in range(len(self.ids.my_list.data)):
            if self.ids.my_list.data[i]['idx'] == index:
                logging.info(f"updating row in interface idx={index} row={updated_row}")
                self.ids.my_list.data[i] = self.row_screen_dict(updated_row)
                return
        log_exception(f"row with idx={index} not found", f"updating row in interface idx={index} row={updated_row}")

    def admit_attendance(self, id_attendance):
        # Here, you can retrieve the events for the given client_id and display them in the user_events screen.
        # You can use the id_event to retrieve the event information from the database.
        logging.debug(f"id_attendance: {id_attendance}")
        updated_row = set_present_true(id_attendance)
        self.update_row(id_attendance, updated_row)
    
    @catch_exceptions
    def search_(self):
        user_input = self.ids.search_input2.text
        logging.debug(f"user filtering from input: {user_input}")
        self.add_rows_for_recycler_view(user_input=user_input)
    
    def add_pointer_focus(self):
        self.ids.search_input2.focus = True

    @catch_exceptions
    def reset_search_timer(self):
        if self._trigger_search:
            self._trigger_search.cancel()
        self._trigger_search = threading.Timer(2.0, self.search_)
        self._trigger_search.start()

    