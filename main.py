from async_agent import *
from dqn_agent import *
import logging

def async_cart_pole():
    config = dict()
    config['task_fn'] = lambda: CartPole()
    config['optimizer_fn'] = lambda params: torch.optim.SGD(params, 0.001)
    config['network_fn'] = lambda: FullyConnectedNet([4, 50, 200, 2])
    config['policy_fn'] = lambda: GreedyPolicy(epsilon=1.0, final_step=5000, min_epsilon=0.1)
    # config['bootstrap_fn'] = OneStepQLearning
    # config['bootstrap_fn'] = NStepQLearning
    config['bootstrap_fn'] = OneStepSarsa
    config['discount'] = 0.99
    config['target_network_update_freq'] = 200
    config['step_limit'] = 300
    config['n_workers'] = 8
    config['batch_size'] = 5
    config['test_interval'] = 500
    config['test_repeats'] = 5
    agent = AsyncAgent(**config)
    agent.run()

def async_lunar_lander():
    config = dict()
    config['task_fn'] = lambda: LunarLander()
    config['optimizer_fn'] = lambda params: torch.optim.Adam(params, 0.001)
    config['network_fn'] = lambda: FullyConnectedNet([8, 50, 200, 4])
    config['policy_fn'] = lambda: GreedyPolicy(epsilon=1.0, final_step=40000, min_epsilon=0.05)
    config['bootstrap_fn'] = OneStepQLearning
    config['discount'] = 0.99
    config['target_network_update_freq'] = 200
    config['step_limit'] = 5000
    config['n_workers'] = 8
    config['batch_size'] = 10
    config['test_interval'] = 1000
    config['test_repeats'] = 5
    agent = AsyncAgent(**config)
    agent.run()

def dqn_cart_pole():
    config = dict()
    config['task_fn'] = lambda: CartPole()
    config['optimizer_fn'] = lambda params: torch.optim.SGD(params, 0.001)
    config['network_fn'] = lambda optimizer_fn: FullyConnectedNet([4, 50, 200, 2], optimizer_fn)
    config['policy_fn'] = lambda: GreedyPolicy(epsilon=1.0, final_step=10000, min_epsilon=0.1)
    config['replay_fn'] = lambda: Replay(memory_size=10000, batch_size=10)
    config['discount'] = 0.99
    config['target_network_update_freq'] = 200
    config['step_limit'] = 0
    config['explore_steps'] = 1000
    config['logger'] = gym.logger
    config['history_length'] = 1
    agent = DQNAgent(**config)
    agent.run()

def actor_critic_cart_pole():
    config = dict()
    config['task_fn'] = lambda: CartPole()
    config['optimizer_fn'] = lambda params: torch.optim.SGD(params, 0.001)
    config['network_fn'] = lambda: ActorCriticNet([4, 200, 2])
    config['policy_fn'] = SamplePolicy
    config['bootstrap_fn'] = AdvantageActorCritic
    config['discount'] = 0.99
    config['target_network_update_freq'] = 200
    config['step_limit'] = 300
    config['n_workers'] = 8
    config['batch_size'] = 5
    config['test_interval'] = 50000
    config['test_repeats'] = 5
    agent = AsyncAgent(**config)
    agent.run()

def dqn_pixel_atari(name):
    config = dict()
    history_length = 4
    config['task_fn'] = lambda: PixelAtari(name, 30)
    config['optimizer_fn'] = lambda params: torch.optim.RMSprop(params, lr=0.00025, alpha=0.95, eps=0.01)
    config['network_fn'] = lambda optimizer_fn: ConvNet(history_length, 6, optimizer_fn)
    config['policy_fn'] = lambda: GreedyPolicy(epsilon=1.0, final_step=1000000, min_epsilon=0.1)
    config['replay_fn'] = lambda: Replay(memory_size=1000000, batch_size=32, dtype=np.uint8)
    config['discount'] = 0.99
    config['target_network_update_freq'] = 10000
    config['step_limit'] = 0
    config['explore_steps'] = 50000
    config['logger'] = gym.logger
    config['history_length'] = history_length
    agent = DQNAgent(**config)
    agent.run()

if __name__ == '__main__':
    gym.logger.setLevel(logging.DEBUG)
    # gym.logger.setLevel(logging.INFO)
    # async_cart_pole()
    # async_lunar_lander()
    # dqn_cart_pole()
    # actor_critic_cart_pole()
    dqn_pixel_atari('Breakout-v0')