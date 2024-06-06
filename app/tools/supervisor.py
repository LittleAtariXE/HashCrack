import multiprocessing
from threading import Thread
from time import sleep


class SuperVisor():
    def __init__(self, hc_callback: object):
        self.name = "SuperVisor"
        self.hc = hc_callback
        self.process_num = self.hc.config.process_number
        self.process = []
        self.lock = multiprocessing.Lock()
        self.threads = []
    
    @property
    def working(self) -> bool:
        return self.hc.working
    
    def is_working(self) -> bool:
        with self.lock:
            if len(self.process) > 0:
                return True
            else:
                return False
    
    def _cleaner(self) -> None:
        while self.working:
            too_clean = []
            with self.lock:
                self.process = [proc for proc in self.process if proc.is_alive()]
            sleep(1)
    
    def cleaner(self) -> None:
        cleaner = Thread(target=self._cleaner, daemon=True)
        cleaner.start()
        self.threads.append(cleaner)

            
    
    def addTask(self, process_obj: object) -> bool:
        if not process_obj:
            return None
        while self.working:
            sleep(1)
            with self.lock:
                if len(self.process) >= self.process_num:
                    continue
                else:
                    process_obj.start()
                    self.process.append(process_obj)
                    return True
    




            
