from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList, TwoLineListItem, ImageLeftWidget
from kivy.lang import Builder
#from db.db_json.clients_handler import get_clients
from db.crud_functions import get_clients

Builder.load_file('list_screen.kv')


class ListScreen(Screen):
    def __init__(self, **kwargs):
        super(ListScreen, self).__init__(**kwargs)
    
    def on_pre_enter(self, *args):
        self.ids.user_list.clear_widgets()
        '''users = [{'firstname': 'John', 'surname': 'Doe', 'cin': '1234567890', 'role': 'Manager', 'firm': 'ACME Inc.'},
                 {'firstname': 'Jane', 'surname': 'Doe', 'cin': '0987654321', 'role': 'Employee', 'firm': 'ACME Inc.'},
                 {'firstname': 'Bob', 'surname': 'Smith', 'cin': '1357908642', 'role': 'Employee', 'firm': 'XYZ Corp'}]'''
        
        # call the get_clients function to retrieve a list of client dictionaries
        users = get_clients()
        for user in users:
            user_item = TwoLineListItem(text=user['firstname'] + " " + user['surname'],
                                        secondary_text=f"[color=0000ff][b]CIN:[/b] {user['cin']}\n"
                                                       f"[color=00ff00][b]Firm:[/b][/color] {user['firm']}\n"
                                                       f"[color=ff0000][b]Role:[/b][/color] {user['role']}",
                                        on_press=lambda e,client_id=user["index"]: self.view_events(client_id),
                                        #markup=True

                                        )
            self.ids.user_list.add_widget(user_item)

    

    def view_events(self, client_id):
        # Here, you can retrieve the events for the given client_id and display them in the user_events screen.
        # You can use the id_event to retrieve the event information from the database.
        print("client_id = ",client_id)
        self.manager.to_user_events_list_screen(client_id=client_id)