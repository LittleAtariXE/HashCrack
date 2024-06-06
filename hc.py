import sys
from app.hash_crack import HashCrack

def parseArgv(args):
    data = {}
    for arg in args[1:]:
        key, value = arg.split("=")
        data[key] = value
    return data

if __name__ == "__main__":
    options = parseArgv(sys.argv)
    HC = HashCrack(**options)
    HC.START()
    

