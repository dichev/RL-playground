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
        states_all = self.env.reset()
        self.rows, self.cols = states_all.shape
        self.values = np.zeros((self.rows, self.cols))
        self.policy_probs = np.full((self.rows, self.cols, 4), 0.25)
        self.explorable_states = self.env.get_explorable_states()

        return self.values, self.policy_probs, states_all

    def config(self, cfg:Config):
        prev = self.cfg
        self.cfg = cfg
        if cfg.greedy_policy != prev.greedy_policy:
            self.policy_iteration()


    def sample(self, pos):
        self.values[pos] = self._calc_value(pos, using_policy=True)
        self.policy_update()
        return self.values, self.policy_probs

    def policy_evaluate(self):
        V = np.zeros_like(self.values)
        # V = self.values
        for pos in self.explorable_states:
            R = self._get_actions_rewards(pos)
            Q = self._get_q_values(pos)
            GAMMA = self.cfg.gamma
            V[pos] = np.sum(self.policy_probs[pos] * (R + GAMMA * Q))

        self.values = V
        return self.values

    def policy_update(self):
        for pos in self.explorable_states:
            if self.cfg.greedy_policy:
                Q = self._get_q_values(pos)
                self.policy_probs[pos] = self._greedy_policy(Q)
            else:
                self.policy_probs[pos] = [0.25,0.25,0.25,0.25]
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
            for pos in self.explorable_states:
                R = self._get_actions_rewards(pos)
                Q = self._get_q_values(pos)
                GAMMA = self.cfg.gamma
                V[pos] = np.max(R + GAMMA * Q)
            self.values = V
        return self.values

    def _get_actions_rewards(self, pos):
        R = [self.env.get_reward(pos, action) for action in range(self.env.num_actions)]
        return R

    def _calc_value(self, pos, using_policy = True):
        assert self.env.is_explorable(pos), f'Trying to calc value of wall: {pos}'

        GAMMA = self.cfg.gamma
        R = [self.env.get_reward(pos, action) for action in range(self.env.num_actions)]
        next_values = self._get_q_values(pos)

        if using_policy:
            v = np.sum( self.policy_probs[pos] * (R + GAMMA * next_values))
        else: # value iteration
            v = np.max(R + GAMMA * next_values)
        return v

    # def calc_q(self, pos, action):
    #     next_pos = self.env.get_next_position(pos, action)
    #     R = self.env.get_reward(pos)
    #     GAMMA = self.cfg.gamma
    #
    #     q = R + GAMMA * self.values[next_pos]
    #     return q

    def _get_q_values(self, pos):
        if self.env.is_terminal(pos):
            return np.zeros(self.env.num_actions)

        next_positions = self.env.get_next_positions_all(pos)
        next_values = [self.values[next_pos] for next_pos in next_positions]
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
