import hashlib
import os
import threading
from art import text2art
from termcolor import cprint
from functools import wraps

from time import sleep

from .tools.config import MrConfig
from .tools.loader import Loader
from .tools.cracker import Cracker
from .tools.supervisor import SuperVisor



class HashCrack:
    def __init__(self, **kwargs):
        self.dir_main = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.config = MrConfig(self, **kwargs)
        self.Loader = Loader(self)
        self.SuperVisor = SuperVisor(self)
        self.makeDirs()
        self.text_name = text2art("<-- Hash Crack -->")
        self.working = False
        self.hashes = []
        self.password_list = []
        self.crack_alg = "sha256"
       

    
    def makeDirs(self) -> None:
        if not os.path.exists(self.config.dir_input):
            os.mkdir(self.config.dir_input)
        if not os.path.exists(self.config.dir_my_combo):
            os.mkdir(self.config.dir_my_combo)
        if not os.path.exists(self.config.dir_output):
            os.mkdir(self.config.dir_output)
        if not os.path.exists(self.config.file_default_out):
            with open(self.config.file_default_out, "w") as f:
                f.write("")
        
    
    def clearScr(self) -> None:
        if os.name == "posix":
            os.system("clear")
        else:
            pass
    
    def intro(self) -> None:
        self.clearScr()
        cprint(self.text_name, "red")
        cprint("\t\t\t\t\t github.com/littleAtariXE", "blue")
        

    def menuMain(self) -> None:
        
        cmd = ""
        while cmd != "q":
            self.intro()
            print("\n\n")
            cprint("<---- Hash Crack Menu: ---->", "red")
            cprint("-- [1] -- Load Hashes to cracking", "blue")
            cprint("-- [2] -- Erase hashes", "blue")
            cprint("-- [3] -- Show all loaded hashes", "blue")
            cprint("-- [4] -- Load password list", "blue")
            cprint("-- [5] -- Status", "blue")
            cprint("-- [6] -- Merge Password list. Making combos", "blue")
            cprint("-- [7] -- Show avaible algorithms", "blue")
            cprint("-- [8] -- Change hash algorithms", "blue")
            cprint("-- [9] -- Start Dictionary Attack", "blue")
            cprint("-- [q] -- Exit Program", "blue")
            cmd = input("<<< ")
            match cmd:
                case "1":
                    self.loadHashMenu()
                case "2":
                    self.eraseHashesMenu()
                case "3":
                    self.showLoadedHashMenu()
                case "4":
                    self.loadPasswordListMenu()
                case "5":
                    self.statusHcMenu()
                case "6":
                    self.mergePasswordListMenu()
                case "7":
                    self.showAvaibleAlgMenu()
                case "8":
                    self.changeHashAlgMenu()
                case "9":
                    self.dictAttack()
                case _:
                    pass


        cprint("[!!] Exit Program [!!]", "red")
    
    def menuDecor(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            rv = func(*args, **kwargs)
            cprint("Press ENTER", "blue")
            input()
            return rv
        return wrapper
    
    @menuDecor
    def loadHashMenu(self) -> None:
        n_hash = self.Loader.menuFileLoad("input", "hashes")
        if not n_hash:
            return
        tmp = set(self.hashes)
        for h in n_hash:
            tmp.add(h)
        self.hashes = list(tmp)
        
    @menuDecor
    def showLoadedHashMenu(self) -> None:
        if len(self.hashes) < 1:
            cprint("No loaded hashes", "red")
        else:
            cprint("All loaded Hashes:", "blue")
            for h in self.hashes:
                cprint(f"{h[0] if h[0] else 'Unknown'} -- {h[1]}", "green")

    
    @menuDecor
    def eraseHashesMenu(self) -> None:
        self.hashes = []
        cprint("Hash list is empty", "green")
    
    @menuDecor
    def loadPasswordListMenu(self) -> None:
        self.password_list = self.Loader.menuFileLoad("library", "passwords")
        cprint(f"Loading {len(self.password_list)} passwords")
    
    @menuDecor
    def statusHcMenu(self) -> None:
        cprint("Status:", "blue")
        cprint(f"Loaded hashes: {len(self.hashes)}", "green")
        cprint(f"Number passwords: {len(self.password_list)}", "green")
        cprint(f"Algorithm Hash: {self.crack_alg}", "green")
        cprint(f"Numbers CPUs used to attack: {self.config.process_number}", "green")
        if len(self.hashes) < 1 or len(self.password_list) < 1:
            cprint(f"Hash Crack is not ready", "red")
        else:
            cprint(f"Hash Crack ready to start", "green")
    
    @menuDecor
    def mergePasswordListMenu(self) -> None:
        cprint("Make new combos", "blue")
        result = self.Loader.mergePassList()
        if not result:
            cprint("[!!] ERROR: Cant make combo list [!!]", "red")
            return
        with open(os.path.join(self.config.dir_lib, result[0]), "w") as file:
            for pasw in result[1]:
                file.write(pasw + "\n")
        cprint(f"Done !!! Check 'library' directory", "green")

    @menuDecor
    def showAvaibleAlgMenu(self) -> None:
        cprint("All Algorithms:", "blue")
        for alg in hashlib.algorithms_available:
            cprint(alg, "green")

    @menuDecor
    def changeHashAlgMenu(self) -> None:
        cprint("Enter algorithms name", "blue")
        alg = input("<<<")
        if not alg in hashlib.algorithms_available:
            cprint(f"[!!] ERROR: Algorithms: {alg} does not exists [!!]")
        else:
            self.crack_alg = alg
            cprint(f"New method: {alg}", "green")
    

    @menuDecor
    def dictAttack(self) -> None:
        if len(self.password_list) < 1 or len(self.hashes) < 1:
            cprint("[!!] ERROR: Hash Crack is not ready. You must loads passwords and hashes [!!]", "red")
            return
        cprint("!!!!! START ATTACK !!!!!!", "blue")
        for index, h_pass in enumerate(self.hashes):
            crack = Cracker(f"Craker_no{index}", self, self.password_list, h_pass[1], self.crack_alg, h_pass[0])
            self.SuperVisor.addTask(crack)
        while self.SuperVisor.is_working():
            sleep(1)
        cprint("All Jobs Done !!! Check output file.", "green")

        
    
    def START(self) -> None:
        self.working = True
        self.SuperVisor.cleaner()
        self.intro()
        cprint("\n\n\n\n\t\t\t\t\t---- Press Enter -------", "blue")
        input()
        self.menuMain()
        self.working = False


        


