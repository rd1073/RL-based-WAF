import numpy as np
import random

class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.99):
        """
        Initialize the Q-learning agent.
        env: The environment the agent will interact with.
        learning_rate: Learning rate for Q-value updates.
        discount_factor: Discount factor for future rewards.
        exploration_rate: Initial exploration rate for the agent.
        exploration_decay: Decay rate for exploration.
        """
        self.env = env
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay

        # Initialize Q-table with dimensions [state, action]
        self.q_table = {}

    def get_state_key(self, state):
        """Return a hashable state representation."""
        return str(state)

    def choose_action(self, state):
        """Choose an action based on the exploration-exploitation tradeoff."""
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(self.env.action_space)  # Explore
        else:
            state_key = self.get_state_key(state)
            if state_key not in self.q_table:
                return random.choice(self.env.action_space)  # Default to random if state not in Q-table
            return np.argmax(self.q_table[state_key])  # Exploit best action

    def update_q_value(self, state, action, reward, next_state):
        """Update the Q-value based on the Q-learning update rule."""
        state_key = self.get_state_key(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = [0] * len(self.env.action_space)

        next_state_key = self.get_state_key(next_state)
        future_q = 0
        if next_state_key in self.q_table:
            future_q = max(self.q_table[next_state_key])

        # Q-learning formula
        self.q_table[state_key][action] += self.learning_rate * (
            reward + self.discount_factor * future_q - self.q_table[state_key][action]
        )

    def train(self, episodes):
        """Train the Q-learning agent."""
        for episode in range(episodes):
            state = self.env.reset()
            total_reward = 0
            while True:
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)

                self.update_q_value(state, action, reward, next_state)

                state = next_state
                total_reward += reward
                if done:
                    break

            # Decay exploration rate
            self.exploration_rate *= self.exploration_decay

            print(f"Episode: {episode + 1}, Total Reward: {total_reward}")

    def evaluate(self, episodes):
        """Evaluate the agent's performance."""
        total_rewards = 0
        for episode in range(episodes):
            state = self.env.reset()
            episode_reward = 0
            while True:
                action = self.choose_action(state)
                _, reward, done = self.env.step(action)
                episode_reward += reward
                if done:
                    break
            total_rewards += episode_reward

        avg_reward = total_rewards / episodes
        
        # Save the model and label encoders
        joblib.dump(svm_ddos_model, 'ddos_model.pkl')
        joblib.dump(scaler, 'scaler.pkl')  # Save the scaler for future use
        joblib.dump(le_src_ip, 'le_src_ip.pkl')
        joblib.dump(le_dst_ip, 'le_dst_ip.pkl')
        joblib.dump(le_label, 'le_label.pkl')

        print(f"Average Reward over {episodes} episodes: {avg_reward}")
