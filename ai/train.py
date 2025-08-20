import numpy as np
import pygame
from ai.flappybird_env import FlappyBirdEnv
from ai.dqn_agent import DQNAgent


class TrainAgent:
    def __init__(self, headless: bool = False):
        """
        Initialize the training agent.

        Args:
            episodes (int): Number of training episodes to run.
            headless (bool): If True, training runs without rendering a window 
                             (faster training, no Pygame events).
        """
        # Training configuration
        self.headless = headless

        # State (input size) and action (output size) dimensions
        self.state_size = 5
        self.action_size = 2

        # Initialize environment (handles its own rendering if not headless)
        self.env = FlappyBirdEnv(mode="ai", headless=self.headless)

        # Initialize the Deep Q-Network (DQN) agent
        self.agent = DQNAgent(self.state_size, self.action_size)

        # Initialize Pygame if not running headless (for rendering and events)
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
            # Reset environment and initialize state
            self.state = np.array(self.env.reset(), dtype=np.float32)
            self.total_reward = 0.0
            self.done = False
            self.step_count = 0

            while not self.done:
                # Handle rendering and user events only if not headless
                if not self.headless:
                    for self.event in pygame.event.get():
                        if self.event.type == pygame.QUIT:
                            self.env.close()
                            pygame.quit()
                            return
                    self.env.render()

                # Choose action using epsilon-greedy strategy
                self.action = self.agent.act(self.state)

                # Perform action in environment
                self.next_state, self.reward, self.done, _ = self.env.step(self.action)
                self.next_state = np.array(self.next_state, dtype=np.float32)

                # Store experience and perform one step of replay
                self.agent.remember(self.state, self.action, self.reward, self.next_state, self.done)
                self.agent.replay()

                # Update state and accumulate metrics
                self.state = self.next_state
                self.total_reward += self.reward
                self.step_count += 1
                
            # Ensure epsilon decays every episode
            if self.agent.epsilon > self.agent.epsilon_min:
                self.agent.epsilon *= self.agent.epsilon_decay

            # Log training progress
            print(
                f"Episode {self.episode_idx + 1}/{self.episodes} | "
                f"Score: {self.env.game.current_score} | "
                f"Reward: {self.total_reward:.2f} | "
                f"Epsilon: {self.agent.epsilon:.4f} | "
                f"Steps: {self.step_count}"
            )

            self.agent.save()

        # Cleanup resources
        self.env.close()
        if not self.headless:
            pygame.quit()



if __name__ == "__main__":
    # Example usage:
    # - headless=True  → fast training without rendering
    # - headless=False → render game window during training
    trainer = TrainAgent(headless=True)
    trainer.train(episodes=500)
