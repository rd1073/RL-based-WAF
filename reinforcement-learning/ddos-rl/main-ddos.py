if __name__ == '__main__':
    # Example dataset of DDoS and legitimate traffic
    combined_dataset = [
        (("192.168.1.1", "192.168.1.100", 5000), 1),  # DDoS attack (high packet rate)
        (("10.0.0.5", "10.0.0.8", 100), 0),  # Legitimate request (normal rate)
        (("172.16.0.3", "172.16.0.5", 6000), 1),  # DDoS attack (high rate)
        (("192.168.2.2", "192.168.2.10", 150), 0)  # Legitimate request (normal rate)
    ]

    # Initialize environment and Q-learning agent
    env = FirewallEnv(combined_dataset)
    agent = QLearningAgent(env)

    # Train the agent
    agent.train(episodes=100)

    # Evaluate the agent
    agent.evaluate(episodes=10)
