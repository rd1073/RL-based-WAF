import numpy as np
import random


class QLearningAgent:
    def __init__(self, env):
        self.env = env
        self.q_table = np.zeros((2, 2))  # 2 states (normal, sqli), 2 actions (block, allow)
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.exploration_rate = 1.0
        self.exploration_decay = 0.99

    def choose_action(self, state_index):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice([0, 1])  # Explore
        else:
            return np.argmax(self.q_table[state_index])  # Exploit

    def update_q_value(self, state_index, action, reward, next_state_index):
        best_next_action = np.argmax(self.q_table[next_state_index])
        td_target = reward + self.discount_factor * self.q_table[next_state_index][best_next_action]
        self.q_table[state_index][action] += self.learning_rate * (td_target - self.q_table[state_index][action])

    def train(self, episodes=1000):
        for _ in range(episodes):
            state = self.env.reset()
            state_index = int(state)  # Convert label to index (0 or 1)
            done = False

            while not done:
                action = self.choose_action(state_index)
                next_state, reward = self.env.step(action)
                next_state_index = int(next_state)
                self.update_q_value(state_index, action, reward, next_state_index)

                state_index = next_state_index
                if self.exploration_rate > 0.1:
                    self.exploration_rate *= self.exploration_decay
