import numpy as np
from game_maze_world import MazeWorld


GAMMA = 1 # 0.9

class Playground:

    def __init__(self):
        self.env = MazeWorld()
        self.reset()

    def reset(self):
        states_all = self.env.reset()
        self.rows, self.cols = states_all.shape
        self.values = np.zeros((self.rows, self.cols))
        self.policy_probs = np.zeros((self.rows, self.cols, 4))

        return self.values, self.policy_probs, states_all

    def sample(self, pos):
        self.values[pos] = self._calc_value(pos)
        self.update_policy()
        return self.values, self.policy_probs

    def evaluate(self, render=True):
        V = np.zeros_like(self.values)
        # V = self.values
        for pos in self._explorable_states():
            V[pos] = self._calc_value(pos)

        self.values = V
        self.update_policy()

        if render: self.render()
        return self.values, self.policy_probs

    def evaluate_times(self, N, render=True):
        for k in range(1, N+1):
            if render: print(f'k = {k}')
            self.evaluate(render=render)
        return self.values, self.policy_probs


    def update_policy(self):
        for pos in self._explorable_states():
            if self.env.is_terminal(pos):
                self.policy_probs[pos] = [0,0,0,0]
            else:
                Q = self._get_q_values(pos)
                self.policy_probs[pos] = self._greedy_policy(Q)


    def _calc_value(self, pos):
        assert self.env.is_explorable(pos), f'Trying to calc value of wall: {pos}'

        R = self.env.get_reward(pos)
        v = R + GAMMA * np.sum(self.policy_probs[pos] * self._get_q_values(pos)) # cfg.greedy_policy
        # v = R + GAMMA * np.sum(0.25 * self._get_q_values(pos)) # todo: cfg.uniform_random_policy
        # todo: this value iteration: v(s) = max(R + sum(prob(a,s') * v(s')) )
        return v

    def _get_q_values(self, pos):  # todo: must be refactored
        assert self.env.is_explorable(pos), f'Trying to get q value of wall: {pos}'
        env = self.env
        return np.array([
            self.values[env.next_pos(pos, env.actions.up)],
            self.values[env.next_pos(pos, env.actions.down)],
            self.values[env.next_pos(pos, env.actions.left)],
            self.values[env.next_pos(pos, env.actions.right)]
        ])

    def _greedy_policy(self, Q):
        max_v = max(Q)
        count = sum([1 for q in Q if q == max_v])
        probs = [1 / count if q == max_v else 0 for q in Q]
        return probs

    def _explorable_states(self):
        for m in range(self.rows):
            for n in range(self.cols):
                if self.env.is_explorable((m,n)):
                    yield m,n

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
    playground.env.render()
    playground.evaluate_times(3)
    print('one more..')
    playground.evaluate()
