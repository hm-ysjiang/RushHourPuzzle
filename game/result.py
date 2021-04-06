class Result:
    def __init__(self, algo, time_elapsed, node_exp, steps, mem_bytes):
        self.algo = algo
        self._time_elapsed = time_elapsed
        self._node_exp = node_exp
        self._steps = steps
        self._mem_bytes = mem_bytes
    
    def get_output(self, detailed, hide_steps):
        return ['Algorithm Performed: %s' % self.algo, self.elapsed, self.expanded_nodes, self.mem_usage, self.steps(False, hide_steps)] if detailed else [self.steps(True, hide_steps)]

    @property
    def elapsed(self):
        return 'Time Elapsed: %.2f sec' % self._time_elapsed

    @property
    def expanded_nodes(self):
        return 'Expanded Nodes: %d' % self._node_exp

    def steps(self, clean, short):
        if short:
            return 'Solution Steps: %d steps' % self._steps.steps
        step_length = len(str(self._steps.steps))
        cur = self._steps
        hist = ''
        while True:
            if cur.steps == 0:
                break
            hist = '%s%s\n%s' % ('' if clean else ('%s: ' % str(cur.steps).zfill(step_length)), cur.hist, hist)
            cur = cur.parent
        return 'Solution Steps: %d steps\n\n' % self._steps.steps + hist.strip()

    @property
    def mem_usage(self):
        unit = 'B'
        disp = self._mem_bytes
        if disp > 1000:
            disp /= 1000
            unit = 'KB'
        if disp > 1000:
            disp /= 1000
            unit = 'MB'
        if disp > 1000:
            disp /= 1000
            unit = 'GB'
        return 'Memory Usage at peak: %.4f %s' % (disp, unit)
