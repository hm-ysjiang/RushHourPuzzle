import argparse
import os
import os.path as path
import re
import subprocess

DIR = path.realpath(path.dirname(__file__))

if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument('algorithm', help='The algorithm to run')
    argp.add_argument('-N', '--no-skip', help='If this is set, the program will re-run all the levels instead of skiping existing levels', action='store_true')
    args = argp.parse_args()
    ALGO = args.algorithm

    levels = [int(re.search(r'L(\d+).txt', entry.name).group(1))
              for entry in os.scandir(path.join(DIR, 'prog1_puzzle'))]
    existing = [int(re.search(r'L(\d+).txt', entry.name).group(1))
              for entry in os.scandir(path.join(DIR, 'output', ALGO))]

    for level in levels:
        if not args.no_skip and level in existing:
            print('Skipping Level %s as it already has an output' % str(level).zfill(2))
            continue
        print('Running %s on Level %s' % (ALGO, str(level).zfill(2)))
        subprocess.run(['python', 'main.py', '-d', '-o',
                        './output/%s/L%%s.txt' % ALGO, str(level), ALGO])
