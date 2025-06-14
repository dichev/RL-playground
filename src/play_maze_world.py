import numpy as np
from dataclasses import dataclass
from game_maze_world import MazeWorld

@dataclass
class Config:
    gamma         :float = 1.0
    greedy_policy :bool  = True # otherwise will be uniform random
    modes                = ['dp_sync_backup', 'dp_inplace_backup', 'dp_prioritized', 'dp_real_time']
    mode          :str   = 'dp_sync_backup'



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
        self.priority = np.zeros((self.rows, self.cols))

        return self.values, self.policy_probs, world

    def config(self, cfg:Config):
        if cfg.mode not in cfg.modes:
            raise Exception(f'There is no such mode: {cfg.mode}')
        prev = self.cfg
        self.cfg = cfg
        if cfg.greedy_policy != prev.greedy_policy:
            self.policy_iteration()

    def get_priority_states(self):
        max_delta = -1
        chosen_state = None
        for state in self.explorable_states:
            if self.priority[state] > max_delta:
                max_delta = self.priority[state]
                chosen_state = state

        states = self.env.get_predecessor_states(chosen_state)
        return states

    def policy_evaluate(self):
        states = self.explorable_states

        if self.cfg.mode == 'dp_sync_backup':
            V = np.zeros_like(self.values) if self.cfg.mode == 'dp_sync_backup' else self.va
        else:
            V = self.values
            if self.cfg.mode == 'dp_prioritized':
                states = self.get_priority_states()

        for state in states:
            R = self._get_actions_rewards(state)
            Vn = self._get_next_states_values(state)
            GAMMA = self.cfg.gamma
            v = np.sum(self.policy_probs[state] * (R + GAMMA * Vn))
            delta = np.abs(self.values[state] - v)
            self.priority[state] = delta
            V[state] = v

        if self.cfg.mode == 'dp_sync_backup':
            self.values = V
        return self.values

    def policy_update(self):
        for state in self.explorable_states:
            if self.cfg.greedy_policy:
                Vn = self._get_next_states_values(state)
                self.policy_probs[state] = self._greedy_policy(Vn)
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
            if self.cfg.mode == 'dp_sync_backup':
                V = np.zeros_like(self.values)
            else:
                V = self.values

            for state in self.explorable_states:
                R = self._get_actions_rewards(state)
                Vn = self._get_next_states_values(state)
                GAMMA = self.cfg.gamma
                V[state] = np.max(R + GAMMA * Vn)

            if self.cfg.mode == 'dp_sync_backup':
                self.values = V
        return self.values

    def _get_actions_rewards(self, state):
        R = [self.env.get_reward(state, action) for action in range(self.env.num_actions)]
        return R

    def _get_next_states_values(self, state):
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
