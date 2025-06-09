import threading
from domains.entity_class import Entity
from domains.model_class import Model
from domains.arch_class import Arch
import canvas
from importlib import reload


class Worker(threading.Thread):
        
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run_reload(self):
        Entity.manager.clear_entity_list()
        Model.manager.clear_model_list()
        Arch.manager.clear_arch_list()
        reload(canvas)
        return canvas.send_data()


