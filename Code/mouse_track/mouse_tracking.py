import csv
import threading
from datetime import datetime, timezone, timedelta
from pynput.mouse import Listener, Button

# Constants\ nKST = timezone(timedelta(hours=9))
CSV_PATH = 'mouse_tracking_our_P29.csv'
FIELDNAMES = ['date', 'hour', 'minute', 'second', 'microsecond', 'x', 'y', 'action', 'dx', 'dy']

class TimeStamp:
    """Utility for current timestamp components in KST."""
    @staticmethod
    def now():
        return datetime.now('KST')

    @classmethod
    def to_list(cls):
        now = cls.now()
        return [
            now.strftime('%Y%m%d'),  # date
            now.strftime('%H'),      # hour
            now.strftime('%M'),      # minute
            now.strftime('%S'),      # second
            str(now.microsecond)     # microsecond
        ]

class MouseLogger:
    def __init__(self, csv_path: str = CSV_PATH):
        self.csv_path = csv_path
        # Write header if file is new
        try:
            with open(self.csv_path, 'x', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(FIELDNAMES)
        except FileExistsError:
            pass

    def log(self, data: list):
        with open(self.csv_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def on_move(self, x, y):
        data = TimeStamp.to_list() + [x, y, 'Move', '', '']
        self.log(data)

    def on_click(self, x, y, button, pressed):
        if button == Button.left:
            action = 'Left' if pressed else 'L_Release'
        elif button == Button.right:
            action = 'Right' if pressed else 'R_Release'
        else:
            action = 'Unknown'
        data = TimeStamp.to_list() + [x, y, action, '', '']
        self.log(data)

    def on_scroll(self, x, y, dx, dy):
        data = TimeStamp.to_list() + [x, y, 'Scroll', dx, dy]
        self.log(data)

    def start(self, daemon: bool = True):
        listener = Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )
        listener_thread = threading.Thread(target=listener.join)
        listener_thread.daemon = daemon
        listener.start()
        listener_thread.start()
        return listener

if __name__ == '__main__':
    logger = MouseLogger()
    print('Starting mouse listener...')
    listener = logger.start()
    try:
        listener.join()
    except KeyboardInterrupt:
        print('Listener stopped by user.')
