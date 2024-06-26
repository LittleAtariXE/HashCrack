import hashlib
import time
from threading import Thread
from termcolor import cprint
from multiprocessing import Process, Lock


class Cracker(Process):
    def __init__(self, name: str, hc_callback: object, password_list: list, hash_password: str, method: str = "md5", login: str = None):
        super().__init__(daemon=True)
        self.name = name
        self.method = getattr(hashlib, method)
        if not self.method:
            cprint(f"[!!] ERROR: Abort Process ! Unknown hash method: {method} [!!]", "red")
            return None
        self.__method = method
        self.pass_list = password_list
        self.hash_pass = hash_password
        self.login = login
        self.encode_format = hc_callback.config.encode_format
        self.out_file = hc_callback.config.file_default_out
        self.lock = Lock()
        self.password = None
        self.done_time = "unknown"
    
    def crackDict(self) -> None:
        start_time = time.time()
        for p in self.pass_list:
            hashed = self.method(p).hexdigest()
            if hashed == self.hash_pass:
                p = p.decode(self.encode_format)
                cprint(f"PASSWORD FINDED !! Found {self.__method} password: {p} ", "green")
                self.password = p
                break
        self.done_time = time.time() - start_time
        self.report()
    
    def report(self) -> None:
        report = "*" * 80
        if not self.password:
            report += "\nPassword not finded\n"
        else:
            report += "\nPaswword finded !!!!!\n"
            report += f"PASSWORD: {self.password}\n"
        if self.login:
            report += f"Login: {self.login}\n"
        else:
            report += "NO LOGIN\n"
        report += f"Hash {self.__method}: {self.hash_pass}\n"
        report += f"Working Time: {round(self.done_time, 2)} sec.\n"
        report += "Attack Type: Dictionary Attack\n"
        report += f"Number of passwords: {len(self.pass_list)}\n"
        report += "*" * 80 + "\n"
        with self.lock:
            with open(self.out_file, "a+") as file:
                file.write(report)
    
    def run(self) -> None:
        cprint(f"Process: {self.name} starting. Hash: {self.hash_pass}", "green")
        self.crackDict()
        cprint(f"Process: {self.name} stopped")
    
        

        


