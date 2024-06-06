import os
import multiprocessing

class MrConfig:
    def __init__(self, hc_callback: object, **kwargs):
        self.hc = hc_callback
        self.encode_format = kwargs.get("encode_format", "utf-8")
        self.dir_main = self.hc.dir_main
        self.dir_lib = os.path.join(self.dir_main, "library")
        self.dir_my_combo = os.path.join(self.dir_lib, "my_combos")
        self.dir_input = os.path.join(self.dir_main, "input")
        self.dir_output = os.path.join(self.dir_main, "output")
        self.file_default_out = os.path.join(self.dir_output, "default.txt")
        self.process_number = kwargs.get("process_num", multiprocessing.cpu_count())

        