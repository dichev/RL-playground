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
        self.world = np.array([
            [W, W, W, W, W, W, W, 0, 0, 0, W, W, G, 0, 0],
            [0, 0, 0, 0, 0, 0, W, 0, W, 0, W, W, 0, 0, 0],
            [W, W, W, W, W, 0, W, W, W, 0, W, W, 0, 0, 0],
            [G, 0, 0, 0, W, 0, 0, 0, 0, 0, W, W, 0, Z, 0],
            [W, W, W, 0, W, 0, W, W, W, 0, W, W, 0, Z, 0],
            [0, 0, 0, 0, W, 0, W, Z, W, 0, W, W, 0, 0, 0],
            [0, W, W, W, W, 0, W, 0, 0, 0, W, W, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, W, W, W, W, W, W, 0, 0, G],
        ])
        self.rows, self.cols = self.world.shape
        self.actions = Actions
        self.num_actions = 4

    def reset(self):
        return self.world


    def get_reward(self, state, action):
        # next_pos = self.get_next_position(pos, action)
        # s = self.world[next_pos] # not the reward of the next state, but of the transition from the current state

        block = self.world[state]

        if   block == 0: return -1
        elif block == G: return +10 # todo: why become 0 in policy iter
        elif block == Z: return -10 # todo: why is not -10 in value iteration
        elif block == W: raise Exception('How u go inside the Wall?')
        else:        raise Exception('check me')


    def render(self):
        out = ''
        for m in range(self.rows):
            for n in range(self.cols):
                s = blocks_dict[self.world[m,n]]
                out += s + ' '
            out += '\n'
        print(out)

    def bound(self, state):
        m, n = state
        return np.clip(m, 0, self.rows-1), np.clip(n, 0, self.cols-1)

    def is_terminal(self, state):
        return self.world[state] == G #or self.world[state] == Z

    def is_explorable(self, state):
        return self.world[state] != W

    def get_explorable_states(self):
        explorable_states = []
        for m in range(self.rows):
            for n in range(self.cols):
                if self.is_explorable((m, n)):
                    explorable_states.append((m, n))
        return explorable_states

    def get_next_state(self, state, action):
        m, n = state
        if   action == Actions.up:    m -= 1
        elif action == Actions.down:  m += 1
        elif action == Actions.left:  n -= 1
        elif action == Actions.right: n += 1

        next_state = self.bound((m, n))
        if self.world[next_state] == W:
            next_state = state

        return next_state

    def get_next_states_all_actions(self, state):
        return [
            self.get_next_state(state, Actions.up),
            self.get_next_state(state, Actions.down),
            self.get_next_state(state, Actions.left),
            self.get_next_state(state, Actions.right)
        ]