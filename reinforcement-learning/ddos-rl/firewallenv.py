import numpy as np
import random

class FirewallEnv:
    def __init__(self, dataset):
        """
        Initialize the environment with a combined dataset.
        dataset: List of tuples with (request_pattern, label), where
                 - request_pattern: A tuple representing request features (e.g., (source_ip, destination_ip, packet_rate))
                 - label: 1 for DDoS attack, 0 for legitimate request
        """
        self.dataset = dataset
        self.action_space = [0, 1]  # 0 = Allow, 1 = Block
        self.state = None
        self.reset()

    def reset(self):
        """Reset the environment to a random request from the dataset."""
        self.state = random.choice(self.dataset)
        return self.state

    def step(self, action):
        """
        Take an action and return the next state, reward, and whether the episode is done.
        action: 0 for Allow, 1 for Block
        """
        request, label = self.state

        # Define rewards
        if action == 1:  # Block
            if label == 1:  # Correctly blocked attack
                reward = 10
            else:  # Incorrectly blocked legitimate request
                reward = -10
        else:  # Allow
            if label == 1:  # Allowed an attack
                reward = -20
            else:  # Correctly allowed a legitimate request
                reward = 5

        # Environment transitions to a new state
        done = True
        self.state = None
        return self.state, reward, done

    def render(self):
        """Display the current state."""
        request, label = self.state
        print(f"Request: {request}, Label: {label}")
