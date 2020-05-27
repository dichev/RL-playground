import random
import numpy as np
import torch
import os

def seed(n = 1):
    random.seed(n)
    np.random.seed(n)
    torch.manual_seed(n)
    torch.cuda.manual_seed_all(n)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    os.environ['PYTHONHASHSEED'] = str(n)
    print(f'[INFO] RNG is seeded to {n}!')

    # test it
    # rnd_python = random.random()
    # rnd_numpy  = np.random.rand(1)[0]
    # rnd_torch  = torch.rand(1).detach().item()
    # try:
    #     assert rnd_python == 0.13436424411240122
    #     assert rnd_numpy  == 0.417022004702574
    #     assert rnd_torch  == 0.7576315999031067
    # except AssertionError as err:
    #     print('The seeded rng don\'t match')
    #     raise

def seed_gym_env(env, n = 1):
    env.action_space.seed(n)
    env.seed(1)
    print(f'[INFO] RNG gym env is seeded to {n}!')