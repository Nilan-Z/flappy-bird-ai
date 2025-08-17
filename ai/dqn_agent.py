import numpy as np
import tensorflow as tf
import yaml
from tensorflow.keras import layers
from collections import deque

class DQNAgent:
    def __init__(self, state_size, action_size):
        # Load config from YAML
        with open("config.yaml", "r") as f:
            cfg = yaml.safe_load(f)

        self.state_size = state_size
        self.action_size = action_size

        # Memory
        self.memory_size = int(cfg.get("memory_size", 20000))
        self.memory = deque(maxlen=self.memory_size)

        # DQN hyperparameters
        self.gamma = float(cfg.get("gamma", 0.99))
        self.epsilon = float(cfg.get("epsilon_start", 1.0))
        self.epsilon_min = float(cfg.get("epsilon_min", 0.01))
        self.epsilon_decay = float(cfg.get("epsilon_decay", 0.995))
        self.batch_size = int(cfg.get("batch_size", 64))
        self.train_start = int(cfg.get("train_start", 1000))

        # Build models
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.update_target_model()
        self.train_steps = 0

    def build_model(self):
        """Build the Q-network model"""
        model = tf.keras.Sequential([
            layers.Dense(64, input_dim=self.state_size, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(
            loss=tf.keras.losses.Huber(),  # more stable than MSE
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001)
        )
        return model

    def update_target_model(self):
        """Copy weights from main model to target model"""
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        """Store experience in memory"""
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """Select action using epsilon-greedy policy"""
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        q_values = self.model.predict(np.array([state]), verbose=0)[0]
        return np.argmax(q_values)

    def replay(self):
        """Train the network using random samples from memory"""
        if len(self.memory) < self.train_start:
            return

        # Safely handle batch size if memory is small
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
                t = self.target_model.predict(np.array([next_state]), verbose=0)[0]
                target[action] = reward + self.gamma * np.amax(t)

            states[i] = state
            targets[i] = target

        self.model.fit(states, targets, epochs=1, verbose=0)

        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        # Optional: update target model periodically
        self.train_steps += 1
        if self.train_steps % 1000 == 0:
            self.update_target_model()
