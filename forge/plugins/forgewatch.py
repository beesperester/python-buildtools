"""Watch module."""

# system
import re
import time

# watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class WatchHandler(FileSystemEventHandler):

    def __init__(self, callbacks, filterExpressions):
        self.callbacks = callbacks
        self.filterExpressions = filterExpressions

        super(WatchHandler, self).__init__()

    def on_modified(self, event):
        trigger = False

        for filterExpression in self.filterExpressions:
            pattern = re.compile(filterExpression)
            
            if pattern.match(event.src_path):
                trigger = True

                break

        if trigger:
            print "{} triggered on_modified event".format(event.src_path)
            for callback in self.callbacks:
                callback()

def watchSrc(src, callbacks=None, **kwargs):
    if callbacks is None:
        callbacks = []

    filterExpressions = []

    if "filter" in kwargs.keys():
        filterExpressions = kwargs["filter"]

        if not isinstance(filterExpressions, list):
            filterExpressions = [filterExpressions]

    def watchWrapper():
        event_handler = WatchHandler(callbacks, filterExpressions)
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