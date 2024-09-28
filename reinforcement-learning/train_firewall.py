import pandas as pd
import numpy as np
from firewall_env import FirewallEnv
from q_learning_agent import QLearningAgent

if __name__ == "__main__":
    # Load your dataset
    dataset_path = "combined_attacks_data.csv"  # Update this with your actual dataset path
    data = pd.read_csv(dataset_path)

    # Initialize environment and agent
    env = FirewallEnv(data)
    agent = QLearningAgent(env)

    # Train the agent
    agent.train(episodes=1000)

    # Save the learned Q-table for future use
    np.save("q_table.npy", agent.q_table)

    print("Training complete. Q-table saved.")
