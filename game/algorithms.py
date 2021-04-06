import queue
import time
import tracemalloc

from .result import Result
from .state import State


def tracer(algo='unknown'):
    def decor(func):
        def wrapper(*args, **kwargs):
            time_start = time.time()
            tracemalloc.start()
            node_exp, steps = func(*args, **kwargs)
            peak_mem_usage = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            return Result(algo, (time.time() - time_start), node_exp, steps, peak_mem_usage)
        return wrapper
    return decor


@tracer('BFS')
def bfs(init_state: State):
    node_exp = 0
    presense = set()
    frontier = queue.Queue()
    presense.add(init_state.hash)
    frontier.put(init_state)
    front = None
    while True:
        front = frontier.get()
        if front.complete:
            break
        for span in front.span():
            if span.hash not in presense:
                presense.add(span.hash)
                frontier.put(span)
                node_exp += 1
    return node_exp, front.history


@tracer('DFS')
def dfs(init_state: State):
    if init_state.complete:
        return 0, init_state.history

    n, d = 0, 0
    presense = set()
    history: list = [init_state.span()]
    node_exp = 0
    presense.add(init_state.hash)
    while True:
        span = next(history[-1], None)
        if span is None:
            history.pop()
        elif span.complete:
            # print(n / d)  # The branching factor
            return node_exp + 1, span.history
        elif span.hash not in presense:
            presense.add(span.hash)
            for _ in span.span():
                n += 1
            history.append(span.span())
            d += 1
            node_exp += 1


@tracer('IDS')
def ids(init_state: State):
    if init_state.complete:
        return 0, init_state.history
    depth = 0
    while True:
        depth += 1

        presense = {}
        history = [init_state.span()]
        node_exp = 0
        presense[init_state.hash] = 0
        while len(history) > 0:
            if depth > 0 and len(history) > depth:
                history.pop()
            span = next(history[-1], None)
            if span is None:
                history.pop()
            elif span.complete:
                return node_exp + 1, span.history
            elif presense.get(span.hash, None) is None or presense.get(span.hash, None) > len(history):
                presense[span.hash] = len(history)
                history.append(span.span())
                node_exp += 1


@tracer('A*')
def astar(init_state: State):
    def F(state: State):
        return state.steps + state.H

    open_queue = queue.PriorityQueue()
    open_dict = {}
    closed_set = set()

    open_queue.put((F(init_state), init_state.hash))
    open_dict[init_state.hash] = init_state

    node_exp, goal_state = 0, None
    while open_queue.qsize() > 0:
        _, state_id = open_queue.get()

        if open_dict[state_id].complete:
            goal_state = open_dict[state_id]
            break
        closed_set.add(state_id)

        for span in open_dict[state_id].span():
            if span.hash in open_dict:
                if span.steps < open_dict[span.hash].steps:
                    up_queue = queue.PriorityQueue()
                    while open_queue.qsize() > 0:
                        f, hash_id = open_queue.get()
                        if hash_id == span.hash:
                            up_queue.put((F(span), span.hash))
                        else:
                            up_queue.put((f, hash_id))
                    open_dict[span.hash] = span
                    open_queue = up_queue
            elif span.hash not in closed_set:
                open_dict[span.hash] = span
                open_queue.put((F(span), span.hash))
                node_exp += 1

        del open_dict[state_id]

    if goal_state:
        return node_exp, goal_state.history
    return 0, []


@tracer('IDA*')
def idastar(init_state: State):
    def F(state: State):
        return state.steps + state.H

    if init_state.complete:
        return 0, init_state.history
    threshold = init_state.H
    while True:
        presense = {}
        history: list = [init_state.span()]
        node_exp = 0
        presense[init_state.hash] = F(init_state)
        min_exceed = None

        while len(history) > 0:
            span = next(history[-1], None)
            if span is None:
                history.pop()
            elif F(span) > threshold:
                min_exceed = F(span) if min_exceed is None else min(min_exceed, F(span))
                continue
            elif span.complete:
                return node_exp + 1, span.history
            elif presense.get(span.hash, None) is None or presense.get(span.hash, None) > F(span):
                presense[span.hash] = F(span)
                history.append(span.span())
                node_exp += 1
        
        threshold = min_exceed


def algo(name: str):
    if name == 'bfs':
        return bfs
    if name == 'dfs':
        return dfs
    if name == 'ids':
        return ids
    if name in ('a-star', 'astar', 'a*'):
        return astar
    if name in ('id-a-star', 'ida-star', 'idastar', 'ida*'):
        return idastar
    return None
