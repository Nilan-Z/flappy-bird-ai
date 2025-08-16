import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from collections import deque

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size

        self.memory = deque(maxlen=20000)
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.batch_size = 64
        self.train_start = 1000

        self.model = self.build_model()
        self.target_model = self.build_model()
        self.update_target_model()

        self.train_steps = 0

    def build_model(self):
        model = tf.keras.Sequential([
            layers.Dense(64, input_dim=self.state_size, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss=tf.keras.losses.Huber(),  # plus stable que MSE
                      optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))
        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        q_values = self.model.predict(np.array([state]), verbose=0)[0]
        return np.argmax(q_values)

    def replay(self):
        if len(self.memory) < self.train_start:
            return

        minibatch = np.random.choice(len(self.memory), self.batch_size, replace=False)
        states = np.zeros((self.batch_size, self.state_size))
        targets = np.zeros((self.batch_size, self.action_size))

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

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        self.train_steps += 1
        if self.train_steps % 1000 == 0:
            self.update_target_model()
