import numpy as np
from dataclasses import dataclass
from game_maze_world import MazeWorld

@dataclass
class Config:
    gamma         :float = 1.0
    greedy_policy :bool  = True # otherwise will be uniform random



class Playground:

    def __init__(self):
        self.env = MazeWorld()
        self.cfg = Config()
        self.reset()

    def reset(self):
        world = self.env.reset()
        self.rows, self.cols = world.shape
        self.values = np.zeros((self.rows, self.cols))
        self.policy_probs = np.full((self.rows, self.cols, 4), 0.25)
        self.explorable_states = self.env.get_explorable_states()

        return self.values, self.policy_probs, world

    def config(self, cfg:Config):
        prev = self.cfg
        self.cfg = cfg
        if cfg.greedy_policy != prev.greedy_policy:
            self.policy_iteration()


    def policy_evaluate(self):
        V = np.zeros_like(self.values)
        # V = self.values
        for state in self.explorable_states:
            R = self._get_actions_rewards(state)
            Q = self._get_q_values(state)
            GAMMA = self.cfg.gamma
            V[state] = np.sum(self.policy_probs[state] * (R + GAMMA * Q))

        self.values = V
        return self.values

    def policy_update(self):
        for state in self.explorable_states:
            if self.cfg.greedy_policy:
                Q = self._get_q_values(state)
                self.policy_probs[state] = self._greedy_policy(Q)
            else:
                self.policy_probs[state] = [0.25,0.25,0.25,0.25]
        return self.policy_probs

    def policy_iteration(self, k=1, render=False):
        for n in range(k):
            self.policy_evaluate()
            self.policy_update()
            if render:
                print(f'k = {n + 1}')
                self.render()
        return self.values, self.policy_probs

    def value_iteration(self, k=1):
        for n in range(k):
            V = np.zeros_like(self.values)
            for state in self.explorable_states:
                R = self._get_actions_rewards(state)
                Q = self._get_q_values(state)
                GAMMA = self.cfg.gamma
                V[state] = np.max(R + GAMMA * Q)
            self.values = V
        return self.values

    def _get_actions_rewards(self, state):
        R = [self.env.get_reward(state, action) for action in range(self.env.num_actions)]
        return R

    def _get_q_values(self, state):
        if self.env.is_terminal(state):
            return np.zeros(self.env.num_actions)

        next_states = self.env.get_next_states_all_actions(state)
        next_values = [self.values[next_state] for next_state in next_states]
        return np.array(next_values)

    def _greedy_policy(self, Q):
        max_v = max(Q)
        max_n = sum([1 for q in Q if q == max_v])
        probs = [1 / max_n if q == max_v else 0. for q in Q]
        return probs


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
    playground.policy_iteration(3, render=True)
