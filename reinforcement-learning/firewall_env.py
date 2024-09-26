import pandas as pd
import numpy as np
import random

class FirewallEnv:
    def __init__(self, data):
        self.data = data
        self.state_space = ["normal", "sqli"]
        self.action_space = [0, 1]  # 0: Block, 1: Allow
        self.current_query_index = None

    def reset(self):
        self.current_query_index = random.randint(0, len(self.data) - 1)
        return self.data.iloc[self.current_query_index]['label']  # return the label of the current query

    def step(self, action):
        label = self.data.iloc[self.current_query_index]['label']
        reward = 0
        if label == 1:  # SQL Injection
            if action == 0:  # Block
                reward = 1  # Good job
            else:  # Allow
                reward = -1  # Bad job
        else:  # Normal
            if action == 1:  # Allow
                reward = 1  # Good job
            else:  # Block
                reward = -1  # Bad job

        # Transition to the next query
        self.current_query_index = random.randint(0, len(self.data) - 1)
        return self.data.iloc[self.current_query_index]['label'], reward
