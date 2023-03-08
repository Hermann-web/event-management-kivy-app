# Event Management System

This is an event management system for a Company that allows the company to keep track of clients and events, as well as which clients are attending which events.
It uses a mongo db database to get clients and events and update attentance.

## Requirements

- Python 3.9.2 (download from python.org)
- pandas (ETL setup)
- pymongo (bdd connection)
- kivy 
- kivymd
- pyinstaller (for desktop targeted packaging)
- opencv-python


## Packaging with PyInstaller 

- Create a virtual environment (optional)
- Install PyInstaller: `pip install pyinstaller`
- Package the application: `pyinstaller --onefile main.py`
- Modify `main.spec` based on `main.spec.example` to include static files (e.g. `.kv` files) and any other required libraries
- Repackage the application: `pyinstaller main.spec`

The packaged application can be found in the `dist` directory.

## Usage

To run the application, navigate to the `dist` directory and run `main.exe`. The application will display a GUI that allows users to view and manage clients and events.

## Logs

Logs can be found in the directory ./share/logs/

## Database

The system connect to a mongo db atlas database with 3 collections:

### Clients

| Column     | Type | Description                                             |
|------------|------|---------------------------------------------------------|
| `index`    | int  | A unique identifier for each client                     |
| `firstname`| str  | The first name of the client                            |
| `surname`  | str  | The surname of the client                                |
| `reference`| str  | A unique reference number for the client                 |
| `firm`     | str  | The company that the client works for                    |
| `role`     | str  | The client's role within the company                     |
| `cin`      | str  | The client's national identification number              |
| `email`    | str  | The client's email address                               |

This database contains information about clients of My Company.

### Events

| Column     | Type | Description                                             |
|------------|------|---------------------------------------------------------|
| `index`    | int  | A unique identifier for each event                      |
| `time`     | str("%H:%M:%S")  | The start time of the event                              |
| `type`     | str(CONF,ATLR,TUTO)  | The type of event (e.g. meeting, conference, presentation)|
| `lecturer` | str  | The name of the person who will deliver the event        |
| `day`      | str(range(1,6))  | The date on which the event will take place              |

This database contains information about events organized by My Company.

### Clients_Events

| Column         | Type  | Description                                                       |
|----------------|-------|-------------------------------------------------------------------|
| `index`        | int   | A unique identifier for each row                                   |
| `id_client`    | int   | The index of the client attending the event                        |
| `id_event`     | int   | The index of the event that the client is attending                 |
| `is_present`   | bool  | A flag indicating whether the client attended the event or not    |
| `time_presence`| str("%H:%M:%S") or null   | The time at which the client arrived at the event                   |

This database contains information about clients attending events organized by My Company.



## Detailled steps for packaging with pyinstaller
 
- create virtual env (or not)
- install pyinstaller (pip install pyinstaller)
- packeging: pyinstaller --onefile main.py 
- change main.spec with the model in main.spec.example
    - add at the top of the file
        ```
        from kivy_deps import sdl2, glew
        from kivymd import hooks_path as kivymd_hooks_path
        ```
    - replace in Analysis path tho the static files(3 kv files)
        ```
        a = Analysis(
            #...,
            datas=[('list_screen.kv', '.'),('list_user_events.kv', '.'),('login_screen.kv', '.')],
            hookspath=[kivymd_hooks_path],
            #...
        )
        ```
    - replace in EXE
        ```
        exe = EXE(
        #...,
        *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
        )
        ```
- repackage the app ```pyinstaller main.spec```
- run the app: It needs the files main.exe, the static files localised as mentioned in main.spec. 


## other ressources

- [practical overview on kivy framework](https://realpython.com/mobile-app-kivy-python/#understanding-the-kivy-framework)
- [python and mongodb](https://www.mongodb.com/languages/python#prerequisites)
- [kivy app packaging with pyinstaller](https://dev.to/ngonidzashe/using-pyinstaller-to-package-kivy-and-kivymd-desktop-apps-2fmj)
- read kivy [app doc](https://kivy.org/doc/stable/api-kivy.app.html) 
- implement recycleview: the [doc](https://kivy.org/doc/stable/api-kivy.uix.recycleview.html) and an [implementation](https://copyprogramming.com/howto/how-to-replace-deprecated-listview-in-kivy)
- customized kivy logger [config](https://kivy.org/doc/stable/api-kivy.logger.html#) and [code source](https://kivy.org/doc/stable/_modules/kivy/logger.html) and [add timestamp to kivy logs](https://groups.google.com/g/kivy-users/c/0M9uaXCC8XA)
