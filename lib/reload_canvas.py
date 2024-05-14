import threading
from domains.entity_class import Entity
import canvas
from importlib import reload


class Worker(threading.Thread):
        
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run_reload(self):
        Entity.manager.clear_entity_list()
        reload(canvas)
        return canvas.send_data()


