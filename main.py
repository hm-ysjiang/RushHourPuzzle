import argparse
import os.path as path

import game.algorithms as algorithms
import game.state as state

DIR = path.dirname(path.realpath(__file__))

if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument(
        'level', help='The level to run the algorithm on', type=int)
    argp.add_argument('algorithm', help='The algorithm to run')
    argp.add_argument(
        '-o', help='Output file format, use %d to indicate the level')
    argp.add_argument('-d', '--detailed',
                      help='Detailed output', action='store_true')
    argp.add_argument('--hide-steps',
                      help='Hide steps in detailed output', action='store_true')
    argp.add_argument('--heuristic',
                      help='The Heuristic used in A* algorithm')
    args = argp.parse_args()
    algo = algorithms.algo(args.algorithm.lower())
    if algo is None:
        argp.error(
            'Unknown algorithm. Available algorithms: bfs, dfs, ids, a-star, ida-star')

    fn = path.join(DIR, 'prog1_puzzle', ('L%s.txt' %
                                         ('%d' % args.level).zfill(2)))
    if not path.isfile(fn):
        argp.error('Cannot find the the specified level')
    with open(fn, 'r') as file:
        puzzle = file.readlines()

    state.__HEURISTIC__ = args.heuristic
    result = algo(state.State.parse(puzzle))
    if args.o is not None:
        with open(path.join(DIR, args.o % str(args.level).zfill(2)), 'w') as file:
            file.write('\n'.join(result.get_output(args.detailed, args.hide_steps)))
    else:
        print()
        print('\n'.join(result.get_output(args.detailed, args.hide_steps)))
