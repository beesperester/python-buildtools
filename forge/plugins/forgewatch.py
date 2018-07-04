"""Watch module."""

# system
import time

# watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class WatchHandler(FileSystemEventHandler):

    def __init__(self, callbacks):
        self.callbacks = callbacks

        super(WatchHandler, self).__init__()

    def on_modified(self, event):
        print "on_modified", event

        for callback in self.callbacks:
            callback()

def watchSrc(src, callbacks=None):
    if callbacks is None:
        callbacks = []

    def watchWrapper():
        event_handler = WatchHandler(callbacks)
        observer = Observer()
        observer.schedule(event_handler, path=src, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            
        observer.join()

    return watchWrapper