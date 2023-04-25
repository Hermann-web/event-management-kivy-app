import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class EventHandler(FileSystemEventHandler):

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print('Restarting script...')
            subprocess.run(['pipenv', 'run', 'python', 'main.py'])


if __name__ == '__main__':
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=True)
    observer.start()
    subprocess.run(['pipenv', 'run', 'python', 'main.py'])
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
