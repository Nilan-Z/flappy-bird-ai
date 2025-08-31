# 🐦 Flappy Bird AI

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A Deep Q-Learning AI that learns to play **Flappy Bird**. 
This project uses TensorFlow and a custom Pygame environment. 

---

## 📚 Table of Contents

- Features
- Note
- Installation
- Configuration
- Usage
- AI Architecture
- Example
- License

---

## 🚀 Features

- Train an AI to play Flappy Bird using **Deep Q-Learning (DQN)**
- Headless mode for accelerated training without graphics
- Manual mode to play the game yourself
- Configurable training and game parameters via `config.yaml`
- Lightweight, minimal, and easily extendable codebase

---

## ⚠️ Note

The AI model included in this repository is **not pre-trained**. 
You need to run the training script before the AI can play effectively:

```bash
python main.py ai --train 5000
```

---

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/Nilan-Z/flappy-bird-ai.git
cd flappy-bird-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Game and AI parameters are defined in config.yaml:

```yaml
screen_width: 288           # Width of the game window
screen_height: 512          # Height of the game window
pipe_gap: 100               # Space between pipes
memory_size: 20000          # Replay memory size for DQN
save_every_n_episodes: 5    # save model every N episodes
batch_size: 64              # Training batch size
learning_rate: 0.001        # DQN learning rate
gamma: 0.99                 # Discount factor
epsilon_start: 1.0          # Starting exploration rate
epsilon_min: 0.01           # Minimum exploration rate
epsilon_decay: 0.995        # Decay rate per step
```

Adjust these values to match your system and training goals.

---

## ▶️ Usage

Run the game after configuring config.yaml:

```bash
python main.py <mode>
```


Modes:

    human — Play manually
    ai — Let the AI play automatically

Training the AI:

Train for a specific number of episodes (recommended):

```bash
python main.py ai --train 5000
```

If no number is provided, training will default to 1 episode:

```bash
python main.py ai --train
```

Optional headless mode for faster training (no graphics):

```bash
python main.py ai --train --headless
```

Notes:

- Training logs show episode, score, reward, epsilon, and steps.
- Trained models are saved automatically.
- For lower-performance machines, reduce memory_size or batch_size to prevent crashes.

---

## 🧠 AI Architecture

The AI is a Deep Q-Network (DQN) implemented with TensorFlow/Keras.
Input: game state (bird position, velocity, distance to pipes, etc.)
Hidden layers: 2 fully connected layers with 64 neurons (ReLU)
Output: Q-values for possible actions (flap or do nothing)
Training: experience replay (deque) + epsilon-greedy exploration

Simplified code:

```python
model = tf.keras.Sequential([
    layers.Dense(64, input_dim=state_size, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(action_size, activation='linear')
])
model.compile(
    loss=tf.keras.losses.Huber(),
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001)
)
```


The agent explores with an ε-greedy strategy, stores transitions in replay memory, and trains with mini-batches to stabilize learning.

---

## 🧾 Example

AI training log:

    Episode 1/1000 | Score: 120 | Reward: 1453.00 | Epsilon: 0.95 | Steps: 14629

Adjust parameters in config.yaml to improve performance.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

