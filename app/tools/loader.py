import os
from termcolor import cprint
from typing import Union
from time import sleep


class Loader:
    def __init__(self, hc_callback: object):
        self.hc = hc_callback
        self.config = self.hc.config
        self.dir_lib = self.hc.config.dir_lib
        self.dir_input = self.hc.config.dir_input
        self.dir_my_combo = self.hc.config.dir_my_combo
    

    def checkFileExist(self, file_name: str, dir_name: str = None) -> Union[None, str]:
        if not dir_name:
            dir_name = self.dir_lib
        fpath = os.path.join(dir_name, file_name)
        if not os.path.exists(fpath):
            cprint(f"[!!] ERROR: File path: {fpath} does not exist [!!]", "red")
            return None
        else:
            return fpath
    

    def loadPasswordFile(self, file_name: str) -> Union[None, list]:
        fpath = self.checkFileExist(file_name)
        if not fpath:
            return None
        data = []
        with open(fpath, "r") as file:
            for line in file.readlines():
                if line == "" or line == "\n":
                    continue
                data.append(line.strip().encode(self.config.encode_format))
        return data
    

    def countLinesFile(self, file_name: str) -> Union[None, int]:
        with open(os.path.join(self.dir_lib, file_name), "r") as file:
            return sum(1 for line in file)
    
    def loadPartFile(self, file_name: str, start_line: int, num_lines: int) -> Union[None, list]:
        fpath = self.checkFileExist(file_name)
        if not fpath:
            return None
        data = []
        with open(fpath, "r") as file:
            for num, line in enumerate(file):
                if num >= start_line:
                    data.append(line)
                if len(data) >= num_lines:
                    break
        return data
    
    def dividePasswords(self, num: int, file_name: str) -> list:
        data = []
        pass_count = self.countLinesFile(file_name)
        nc = pass_count // num
        ncc = pass_count % num
        for x in range(num):
            tmp = []
            if x == (num - 1):
                part = self.loadPartFile(file_name, (x * nc), nc + ncc)
            else:
                part = self.loadPartFile(file_name, (x * nc), nc)
            data.append(part)
        
        return data
    
    def loadHashes(self, file_name: str) -> Union[list, None]:
        fpath = self.checkFileExist(file_name, self.dir_input)
        if not fpath:
            cprint(f"[!!] ERROR: File: {file_name} does not exists in input dir [!!]", "red")
            return None
        hashes = []
        with open(fpath, "r") as file:
            for line in file.readlines():
                if line == "\n" or line == "":
                    continue
                if ":" in line:
                    login = line[0:line.find(":")]
                    to_crack = line[line.find(":") + 1:]
                else:
                    login = None
                    to_crack = line
                hashes.append((login, to_crack.strip()))
        cprint(f"Loaded hashes to be cracked", "green")
        return hashes
    
    def menuFileLoad(self, dir_name: str, types: str) -> Union[str, list, None]:
        menu = {}
        c = 0
        main_dir = os.path.join(self.hc.config.dir_main, dir_name)
        for f in os.listdir(main_dir):
            if os.path.isdir(os.path.join(main_dir, f)):
                continue
            c += 1
            menu[str(c)] = (f, os.path.join(main_dir, f))
        self.hc.intro()
        cprint("\n\nChoose file to load. Enter ID:", "green")
        for k, i in menu.items():
            cprint(f"[{k}]  -  {i[0]}", "blue")
        chose = input("ID <<< ")
        chose = menu.get(chose)
        if not chose:
            cprint("[!!] ERROR: File does not exists [!!]", "red")
            sleep(2)
            return None
        if types == "hashes":
            data = self.loadHashes(chose[0])
            return data
        elif types == "passwords":
            data = self.loadPasswordFile(chose[0])
            return data
    
    
    def mergePassList(self, name: str = "My_Combos.txt") -> None:
        combo = set()
        try:
            for fp in os.listdir(self.dir_my_combo):
                for pasw in self.loadPasswordFile(fp):
                    combo.add(pasw.decode(self.hc.config.encode_format))
            return (name, combo)
        except Exception as e:
            cprint(f"[!!] ERROR: {e} [!!]", "red")
            return None
        

        

    

                

        


