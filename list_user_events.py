## list_user_events.py
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList, TwoLineListItem, ImageLeftWidget
from kivy.lang import Builder
#from db.db_json.clients_handler import  filter_client_choices
from db.crud_functions import filter_client_choices

Builder.load_file('list_user_events.kv')


class ListUserEventsScreen(Screen):
    def __init__(self, **kwargs):
        super(ListUserEventsScreen, self).__init__(**kwargs)
    
    def on_pre_enter(self, *args):
        self.ids.user_event_list.clear_widgets()
        client_id = self.manager.data.get("client_id")
        event_id = self.manager.data.get("event_id")
        day = self.manager.data.get("day")
        hour = self.manager.data.get("hour")
        print("client_id landed: ",client_id)
        # call the get_clients function to retrieve a list of client dictionaries
        user_events = filter_client_choices(id_client=client_id, id_event=event_id, day=day, hour=hour)
        for user in user_events:
            user_item = TwoLineListItem(
                    text=f"event n° {user['id_event']}",
                    secondary_text=f"[color=0000ff][b]client n°:[/b] {user['id_client']}\n"
                                    f"[color=0000ff][b]is_present:[/b] {user['is_present']}\n"
                                    f"[color=00ff00][b]time_presence:[/b][/color] {user['time_presence']}"
                    )
            self.ids.user_event_list.add_widget(user_item)

    