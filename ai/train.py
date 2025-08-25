import numpy as np
import pygame
import yaml
from ai.flappybird_env import FlappyBirdEnv
from ai.dqn_agent import DQNAgent
from datetime import datetime

class TrainAgent:
    def __init__(self, headless: bool = False):
        # Load configuration
        with open("config.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        self.save_every_n_episodes = int(cfg.get("save_every_n_episodes", 50))
        self.headless = headless

        # State (input) and action (output) dimensions
        self.state_size = 5
        self.action_size = 2

        # Initialize environment and agent
        self.env = FlappyBirdEnv(mode="ai", headless=self.headless)
        self.agent = DQNAgent(self.state_size, self.action_size)

        # Initialize Pygame window if not headless
        if not self.headless:
            pygame.init()
            pygame.display.set_caption("Flappy Bird AI Training")

        # Training metrics
        self.total_reward = 0.0
        self.done = False
        self.step_count = 0

    def train(self, episodes: int = 500):
        # Run training loop for the given number of episodes
        self.episodes = episodes
        
        for self.episode_idx in range(self.episodes):
            # Reset environment at the start of each episode
            self.state = np.array(self.env.reset(), dtype=np.float32)
            self.total_reward = 0.0
            self.done = False
            self.step_count = 0

            while not self.done:
                # Handle Pygame events if rendering is enabled
                if not self.headless:
                    for self.event in pygame.event.get():
                        if self.event.type == pygame.QUIT:
                            self.env.close()
                            pygame.quit()
                            return
                    self.env.render()

                # Select action and perform environment step
                self.action = self.agent.act(self.state)
                self.next_state, self.reward, self.done, _ = self.env.step(self.action)
                self.next_state = np.array(self.next_state, dtype=np.float32)

                # Store experience and train from replay buffer
                self.agent.remember(self.state, self.action, self.reward, self.next_state, self.done)
                self.agent.replay()

                # Update state and accumulate metrics
                self.state = self.next_state
                self.total_reward += self.reward
                self.step_count += 1

            # Decay exploration rate epsilon
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

            # Save model every N episodes or at the last episode
            if (self.episode_idx + 1) % self.save_every_n_episodes == 0 or self.episode_idx == self.episodes - 1:
                self.agent.save()

        # Cleanup after training
        self.env.close()
        if not self.headless:
            pygame.quit()
    
    def log_message(self, message: str, log_file: str = "training.log"):
        # Append message to log file with timestamp and print to console
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"[{timestamp}] {message}")

if __name__ == "__main__":
    # Exemple d'entraînement sans affichage
    trainer = TrainAgent(headless=True)
    trainer.train(episodes=500)
