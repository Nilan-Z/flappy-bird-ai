# flappy-bird-ai

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An AI-powered version of Flappy Bird written in Python with **Pygame** for graphics and **Deep Q-Learning (DQN)** for training the bird to play autonomously.  
Includes manual gameplay mode, AI inference mode, and full training pipeline with TensorFlow/Keras.

## 📚 Table of Contents

- Installation
- Usage
- License


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

## ▶️ Usage

After configuring `config.yaml`, run the game with:

```bash
python main.py <user>
```

`<user>` can be:

- `human` — to play manually
- `ai` — to let the AI play

To train the AI, use:

```bash
python main.py ai --train
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

