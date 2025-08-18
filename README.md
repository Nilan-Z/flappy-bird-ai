# 🐦 Flappy Bird AI

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A Deep Q-Learning AI that learns to play **Flappy Bird**. 
This project uses TensorFlow and a custom Pygame environment. 

---

## 📚 Table of Contents

- Features
- Installation
- Configuration
- Usage
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

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/YourUsername/flappy-bird-ai.git
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
screen_width: 288       # Width of the game window
screen_height: 512      # Height of the game window
pipe_gap: 100           # Space between pipes
memory_size: 20000      # Replay memory size for DQN
batch_size: 64          # Training batch size
learning_rate: 0.001    # DQN learning rate
gamma: 0.99             # Discount factor
epsilon_start: 1.0      # Starting exploration rate
epsilon_min: 0.01       # Minimum exploration rate
epsilon_decay: 0.995    # Decay rate per step
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


python main.py ai --train 5000

```bash
If no number is provided, training will default to 1 episode:
```

```bash
python main.py ai --train
```

Optional headless mode for faster training (no graphics):

```bash
python main.py ai --train --headless
```

Notes:

-Training logs show episode, score, reward, epsilon, and steps.
-Trained models are saved automatically.
-For lower-performance machines, reduce memory_size or batch_size to prevent crashes.

---

## 🧾 Example

AI training log:

    Episode 1/1000 | Score: 0 | Reward: -5.30 | Epsilon: 1.00 | Steps: 48

Adjust parameters in config.yaml to improve performance.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

