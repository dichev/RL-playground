import numpy as np

W = 1 # wall
G = 2 # goal
Z = 3 # trap (electricity)
A = 4 # agent
blocks_dict = { 0: '.', 1: 'W', 2: 'G', 3: 'Z', 4: 'A'}

class Actions:
    up    = 0
    down  = 1
    left  = 2
    right = 3


class MazeWorld:

    def __init__(self):
        self.state = np.array([
            [W, W, W, W, W, W, W, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, W, 0, W, 0],
            [W, W, W, W, W, 0, W, W, W, 0],
            [G, 0, 0, 0, W, 0, 0, 0, 0, 0],
            [W, W, W, 0, W, 0, W, W, W, 0],
            [0, 0, 0, 0, W, 0, W, Z, W, 0],
            [0, W, W, W, W, 0, W, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, W, W, W, W],
        ])
        self.rows, self.cols = self.state.shape
        self.actions = Actions

    def reset(self):
        return self.state

    def get_reward(self, position):
        m, n = position
        if   m < 0: m = 0
        elif m > self.rows-1: m = self.rows-1
        if   n < 0: n = 0
        elif n > self.cols-1: n = self.cols-1

        s = self.state[m, n]
        if   s == 0: return -1
        elif s == G: return 10
        elif s == Z: return -10
        elif s == W: raise Exception('How u go inside the Wall?')
        else:        raise Exception('check me')


    def render(self):
        out = ''
        for m in range(self.rows):
            for n in range(self.cols):
                s = blocks_dict[self.state[m,n]]
                out += s + ' '
            out += '\n'
        print(out)

    def bound(self, pos):
        m, n = pos
        return np.clip(m, 0, self.rows-1), np.clip(n, 0, self.cols-1)

    def is_terminal(self, pos):
        return self.state[pos] == G

    def is_explorable(self, pos):
        return self.state[pos] != W

    def next_pos(self, pos, action):
        m, n = pos
        if   action == Actions.up:    m -= 1
        elif action == Actions.down:  m += 1
        elif action == Actions.left:  n -= 1
        elif action == Actions.right: n += 1

        next_pos = self.bound((m, n))

        if self.state[next_pos] == W:
            return pos
        else:
            return next_pos

