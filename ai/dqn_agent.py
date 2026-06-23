import os
from collections import deque
from typing import Tuple

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import Huber
import logging

from flappybird.path_utils import load_yaml_config, resolve_project_path

# Configure logger
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')


class DQNAgent:
    """Deep Q-Network agent for reinforcement learning tasks."""

    def __init__(self, state_size: int, action_size: int,
                 model_path: str = "ai/dqn_model.keras",
                 training: bool = True):
        """
        Initialize DQN agent.

        Args:
            state_size: Number of input features.
            action_size: Number of possible actions.
            model_path: Path to save/load model weights.
            training: Whether the agent is in training mode.
        """
        self.state_size = state_size
        self.action_size = action_size
        self.model_path = str(resolve_project_path(model_path)) if not os.path.isabs(model_path) else model_path
        self.training = training

        # Load configuration
        cfg = load_yaml_config()

        # Memory
        self.memory_size = int(cfg.get("memory_size", 20000))
        self.memory: deque = deque(maxlen=self.memory_size)

        # Hyperparameters
        self.gamma: float = float(cfg.get("gamma", 0.99))
        self.epsilon_min: float = float(cfg.get("epsilon_min", 0.01))
        self.epsilon_decay: float = float(cfg.get("epsilon_decay", 0.995))
        self.batch_size: int = int(cfg.get("batch_size", 64))
        self.train_start: int = int(cfg.get("train_start", 1000))
        self.epsilon: float = float(cfg.get("epsilon_start", 1.0)) if training else self.epsilon_min

        self.train_steps: int = 0
        self.model: Sequential = self.build_model()

        if os.path.exists(self.model_path):
            self.load()
        else:
            logging.warning("No saved model found, starting with a new model.")

    def build_model(self) -> Sequential:
        """Build the neural network model for the agent."""
        model = Sequential([
            layers.Dense(64, input_dim=self.state_size, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss=Huber(), optimizer=Adam(learning_rate=0.001))
        return model

    def remember(self, state: np.ndarray, action: int,
                 reward: float, next_state: np.ndarray, done: bool) -> None:
        """Store experience in replay memory."""
        if self.training:
            self.memory.append((state, action, reward, next_state, done))

    def act(self, state: np.ndarray) -> int:
        """Choose action based on epsilon-greedy policy."""
        if self.training and np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        q_values = self.model.predict(np.array([state]), verbose=0)[0]
        return int(np.argmax(q_values))

    def replay(self) -> None:
        """Train the network using a batch sampled from memory."""
        if not self.training or len(self.memory) < self.train_start:
            return

        batch_size = min(self.batch_size, len(self.memory))
        minibatch = np.random.choice(len(self.memory), batch_size, replace=False)

        states = np.zeros((batch_size, self.state_size))
        targets = np.zeros((batch_size, self.action_size))

        for i, idx in enumerate(minibatch):
            state, action, reward, next_state, done = self.memory[idx]
            target = self.model.predict(np.array([state]), verbose=0)[0]
            if done:
                target[action] = reward
            else:
                t = self.model.predict(np.array([next_state]), verbose=0)[0]
                target[action] = reward + self.gamma * np.amax(t)
            states[i] = state
            targets[i] = target

        self.model.fit(states, targets, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        self.train_steps += 1

    def save(self, path: str = None) -> None:
        """Save model weights to disk."""
        if path is None:
            path = self.model_path
        self.model.save_weights(path)
        logging.info(f"Model saved to {path}")

    def load(self, path: str = None) -> None:
        """Load model weights from disk if available."""
        if path is None:
            path = self.model_path
        if os.path.exists(path):
            self.model.load_weights(path)
            logging.info(f"Model loaded from {path}")
        else:
            logging.warning(f"Model file {path} does not exist.")
