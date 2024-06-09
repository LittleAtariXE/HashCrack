import hashlib
import string
import multiprocessing
import itertools
import time
import sys
from multiprocessing import Process
from termcolor import cprint


class Brutus:
    def __init__(self, hc_callback: object):
        self.name = "Brutus"
        self.hc = hc_callback
        self.combos = None
        self.combo_hit = None
    
    def prepareCombo(self):
        self.hc.clearScr()
        self.hc.intro()
        cprint("----- Chose Combo ------", "blue")
        cprint(f"-- [1] -- Lower chars:\n\t\t'{string.ascii_lowercase}'", "blue")
        cprint(f"-- [2] -- Upper chars\n\t\t'{string.ascii_uppercase}'", "blue")
        cprint(f"-- [3] -- Lower + Upper chars\n\t\t'{string.ascii_lowercase}{string.ascii_uppercase}", "blue")
        cprint(f"-- [4] -- Only numbers\n\t\t'{string.digits}'", "blue")
        cprint(f"-- [5] -- All chars + numbers\n\t\t'{string.ascii_letters}{string.digits}'", "blue")
        combo_type = input("<<<")
        match combo_type:
            case "1":
                self.combos = string.ascii_lowercase
            case "2":
                self.combos = string.ascii_uppercase
            case "3":
                self.combos = string.ascii_lowercase + string.ascii_uppercase
            case "4":
                self.combos = string.digits
            case "5":
                self.combos = string.ascii_letters + string.digits
            case _:
                return
        self.combos = list(self.combos)
        cprint("The given number of characters will check each combination starting from one character", "blue")
        cprint("If you put a '$' sign before a number, combinations with only that number of characters will be used", "blue")
        self.combo_hit = input("Number of chars: ")
        
    
    def check(self) -> bool:
        if not self.combo_hit or not self.combos:
            return False
        else:
            return True
        
        

class BruteForce(Process):
    def __init__(self, name: str, hc_callback: object, combos: list, combo_hit: str, hash_password: str, method: str = "sha256", login: str = None):
        super().__init__(daemon=True)
        self.name = name
        self.encode_format = hc_callback.config.encode_format
        self.out_file = hc_callback.config.file_default_out
        self.__method = method
        self.method = getattr(hashlib, method)
        if not self.method:
            cprint(f"[!!] ERROR: Abort Process ! Unknown hash method: {method} [!!]", "red")
            return None
        self.combo_scheme = combos
        self.hash_pass = hash_password
        self.login = login
        self.lock = multiprocessing.Lock()
        self.combo_hit = combo_hit
        self.done_time = "Unknown"
        self.hit_num = 0
        self.password = None
        self.matched_hits = None
    

    def matchHits(self) -> str:
        num_hits = 0
        for c in range(self.first_hit, self.last_hit + 1):
            combo = len(self.combo_scheme) ** c
            num_hits += combo
        return str(num_hits)
    
    def prepareAttack(self) -> bool:
        if self.combo_hit.startswith("$"):
            try:
                self.last_hit = int(self.combo_hit.lstrip("$"))
                self.first_hit = self.last_hit
            except ValueError:
                cprint("[!!] ERROR: Value must be INT [!!]", "red")
                return None
        else:
            try:
                self.last_hit = int(self.combo_hit)
                self.first_hit = 1
            except ValueError:
                cprint("[!!] ERROR: Value must be INT [!!]", "red")
                return None
        return True
    
    def attack(self):
        self.matched_hits = self.matchHits()
        cprint(f"number of attack combinations: {self.matched_hits}")
        start = time.time()
        for c in range(self.first_hit, self.last_hit + 1):
            combos = itertools.product(self.combo_scheme, repeat=c)
            for hit in combos:
                self.hit_num += 1
                punch = "".join(hit).encode(self.encode_format)
                hashed = self.method(punch).hexdigest()
                if hashed == self.hash_pass:
                    p = punch.decode(self.encode_format)
                    cprint(f"PASSWORD FINDED !! Found {self.__method} password: {p} ", "green")
                    self.password = p
                    break
        self.done_time = time.time() - start
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
        report += "Attack Type: BruteForce\n"
        report += f"Number of combinations: {self.hit_num} / {self.matched_hits}\n"
        report += "*" * 80 + "\n"
        with self.lock:
            with open(self.out_file, "a+") as file:
                file.write(report)       
    
    def run(self) -> None:
        cprint(f"Process: {self.name} starting. Hash: {self.hash_pass}", "green")
        self.attack()
        cprint(f"Process: {self.name} stopped")

        
        

    













