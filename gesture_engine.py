import threading
import handsfree

class GestureEngine:
    def __init__(self):
        self.running = False
        self.frame = None
        self.current_gesture = "None"
        self.lock = threading.Lock()

    def start(self):
        self.running = True
        handsfree.main(self)   # call your backend

    def stop(self):
        self.running = False

    def update_frame(self, frame):
        with self.lock:
            self.frame = frame.copy()

    def get_frame(self):
        with self.lock:
            return self.frame

    def update_gesture(self, gesture):
        self.current_gesture = gesture