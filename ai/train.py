import numpy as np
import pygame
from ai.flappybird_env import FlappyBirdEnv
from ai.dqn_agent import DQNAgent
from datetime import datetime



class TrainAgent:
    def __init__(self, headless: bool = False):
        """
        Training loop manager for the Flappy Bird DQN agent.

        Args:
            headless: If True, training runs without rendering a window 
                      (faster training, no Pygame events).
        """
        self.headless = headless

        # State (input) and action (output) dimensions for the agent
        self.state_size = 5
        self.action_size = 2

        # Initialize Flappy Bird environment
        self.env = FlappyBirdEnv(mode="ai", headless=self.headless)

        # Initialize the Deep Q-Network (DQN) agent
        self.agent = DQNAgent(self.state_size, self.action_size)

        # Pygame setup only if rendering is enabled
        if not self.headless:
            pygame.init()
            pygame.display.set_caption("Flappy Bird AI Training")

        # Metrics
        self.total_reward = 0.0
        self.done = False
        self.step_count = 0

    def train(self, episodes: int = 500):
        """
        Run the training loop for the specified number of episodes.
        """
        self.episodes = episodes
        
        for self.episode_idx in range(self.episodes):
            # Reset environment at start of each episode
            self.state = np.array(self.env.reset(), dtype=np.float32)
            self.total_reward = 0.0
            self.done = False
            self.step_count = 0

            # Episode loop
            while not self.done:
                # Handle rendering and user events only if not headless
                if not self.headless:
                    for self.event in pygame.event.get():
                        if self.event.type == pygame.QUIT:
                            self.env.close()
                            pygame.quit()
                            return
                    self.env.render()

                # Select action (epsilon-greedy policy)
                self.action = self.agent.act(self.state)

                # Perform action in environment
                self.next_state, self.reward, self.done, _ = self.env.step(self.action)
                self.next_state = np.array(self.next_state, dtype=np.float32)

                # Store experience and train from replay buffer
                self.agent.remember(self.state, self.action, self.reward, self.next_state, self.done)
                self.agent.replay()

                # Update state and accumulate metrics
                self.state = self.next_state
                self.total_reward += self.reward
                self.step_count += 1
                
            # Decay exploration rate (epsilon) at the end of each episode
            if self.agent.epsilon > self.agent.epsilon_min:
                self.agent.epsilon *= self.agent.epsilon_decay

            # Log episode results
            self.log_message(
                f"Episode {self.episode_idx + 1}/{self.episodes} | "
                f"Score: {self.env.game.current_score} | "
                f"Reward: {self.total_reward:.2f} | "
                f"Epsilon: {self.agent.epsilon:.4f} | "
                f"Steps: {self.step_count}"
            )

            # Save agent model weights
            self.agent.save()

        # Cleanup resources after training completes
        self.env.close()
        if not self.headless:
            pygame.quit()
    
    def log_message(self, message: str, log_file: str = "training.log"):
        """
        Append a message to a log file with a timestamp.

        Args:
            message (str): The text to log.
            log_file (str): Path to the log file (default: training.log).
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"[{timestamp}] {message}")  # garde aussi l'affichage console

if __name__ == "__main__":
    # Example usage:
    # - headless=True  → fast training without rendering
    # - headless=False → render game window during training
    trainer = TrainAgent(headless=True)
    trainer.train(episodes=500)
