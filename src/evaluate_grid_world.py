import numpy as np
from shared.lib.utils import AttrDict, dict_as_object
from enum import Enum
import copy

# Env ---------------------------------------

GAMMA = 1#0.9

W = 1 # wall
G = 2 # goal
Z = 3 # electricity
A = 4 # agent


# class Blocks(Enum):
#     W = 1
#     G = 2
#     Z = 3
#     A = 4


tmp = {
    0: '.',
    1: 'W',
    2: 'G',
    3: 'Z',
    4: 'A',
}

'''
|
|___ |
|__  |
|__| |
|____|

'''

# Actions ---------------------------------------
class Actions:
    up    = 0
    down  = 1
    left  = 2
    right = 3


class GridWorld:

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
        self.actions = AttrDict(
            up    = 0,
            down  = 1,
            left  = 2,
            right = 3,
        )
        self.agent_pos = (3,3)
        self.terminal = np.array((self.state == Z) + (self.state == G))
        self.walls = np.array((self.state == W))


    def get_reward(self, position):

        m, n = position
        if m < 0: m = 0
        if m > self.state.shape[0]-1: m = self.state.shape[0]-1
        if n < 0: n = 0
        if n > self.state.shape[1]-1: n = self.state.shape[1]-1

        s = self.state[m, n]
        if   s == 0: return -1
        elif s == G: return 10
        elif s == Z: return -10
        elif s == W: raise Exception('How u go inside the Wall?')
        else:        raise Exception('check me')

    def step(self, action):
        m, n = self.agent_pos
        if action == self.actions.up:
            m -= 1
        elif action == self.actions.down:
            m += 1
        elif action == self.actions.left:
            n -= 1
        elif action == self.actions.right:
            n += 1


        #if self.state[m, n] != W:
        self.agent_pos = self.bound((m,n))


        reward = self.get_reward(self.agent_pos)
        self.render()
        return reward


    def render(self):
        out = ''
        for m in range(self.state.shape[0]):
            for n in range(self.state.shape[1]):
                if self.agent_pos == (m,n):
                    s = 'A'
                else:
                    s = tmp[self.state[m,n]]
                out += s + ' '
            out += '\n'
        print(out)

    def bound(self, pos):
        m, n = pos
        return np.clip(m, 0, self.rows - 1), np.clip(n, 0, self.cols - 1)

    def next_pos(self, pos, action):
        m, n = pos
        if action == self.actions.up:
            m -= 1
        elif action == self.actions.down:
            m += 1
        elif action == self.actions.left:
            n -= 1
        elif action == self.actions.right:
            n += 1

        next_pos = self.bound((m, n))

        if self.state[next_pos] == W:
            return pos
        else:
            return next_pos



class Playground:

    def __init__(self):
        self.env = GridWorld()
        self.rows, self.cols = self.env.state.shape
        self.reset()

    def reset(self):
        self.values = np.zeros_like(self.env.state).astype('float32')
        self.policy_probs = np.zeros((*self.env.state.shape, 4)) + [0.25, 0.25, 0.25, 0.25]
        self.policy_probs[self.env.terminal + self.env.walls] = 0

        return self.values, self.policy_probs, self.env.state

    def calc_value(self, position):
        # assert not self.env.terminal[position], f'Trying to calc value of terminal state: {position}'
        env = self.env
        m, n = position
        R = env.get_reward((m, n))
        v = R + np.sum(self.policy_probs[m,n] * self.get_q_values(position))
        # v = R + np.sum(0.25 * self.get_q_values(position)) * GAMMA
        return v

    def update_policy(self):
        for m in range(self.rows):
            for n in range(self.cols):
                if not self.env.terminal[m, n] and not self.env.walls[m,n]:
                    Q = self.get_q_values((m,n))
                    max_v = max(Q)
                    self.policy_probs[m, n] = [ 1 if q == max_v else 0 for q in Q] # todo sum(probs) > 1
        pass

    def get_q_values(self, pos):  # todo: must be refactored
        # if self.env.terminal[pos]: return 0
        # if self.env.walls[pos]: return 0
        assert not self.env.walls[pos], f'Trying to get q value of wall: {pos}'

        V, env = self.values, self.env
        return np.array([
            V[env.next_pos(pos, env.actions.up)],
            V[env.next_pos(pos, env.actions.down)],
            V[env.next_pos(pos, env.actions.left)],
            V[env.next_pos(pos, env.actions.right)]
        ])

    def sample(self, position):
        self.values[position] = self.calc_value(position)
        self.update_policy()
        return self.values, self.policy_probs

    def evaluate(self, render=True):
        V = np.zeros_like(self.values)
        # V = values
        for m in range(self.rows):  # todo: use ndarray operation
            for n in range(self.cols):
                if not self.env.walls[m,n]:
                    V[m, n] = self.calc_value((m,n))

        self.values = V
        self.update_policy()

        if render: self.render()
        return self.values, self.policy_probs

    def evaluate_times(self, N, render=True):
        for k in range(1, N+1):
            if render: print(f'k = {k}')
            self.evaluate(render=render)
        return self.values, self.policy_probs

    def render(self):
        env, values, rows, cols = self.env, self.values, self.rows, self.cols
        out = ''
        for m in range(rows):
            for n in range(cols):
                v = values[m, n]
                out += (' ' if v >= 0 else '') + f'{v:.2f} '
            out += '\n'
        print(out)


if __name__ == "__main__":
    playground = Playground()
    playground.evaluate_times(10)
    print('one more..')
    playground.evaluate()
