import os
import os.path as path
import re

DIR = path.realpath(path.dirname(__file__))
ALGO = 'idastar'

time = 0
mem = 0
exp = 0

if __name__ == '__main__':
    for entry in os.scandir(path.join(DIR, 'output', ALGO)):
        with open(path.join(DIR, 'output', ALGO, entry.name), 'r') as file:
            data = file.readlines()[1:5]
        m = re.search(r'.* (\d+\.\d+) sec', data[0])
        time += float(m.group(1))

        m = re.search(r'.* (\d+)', data[1])
        exp += int(m.group(1))
        
        m = re.search(r'.* (\d+\.\d+) (.+)', data[2])
        mem += float(m.group(1)) * (1 if m.group(2) == 'KB' else 1000)
    print(time / 19)
    print(mem / 19)
    print(exp / 19)
