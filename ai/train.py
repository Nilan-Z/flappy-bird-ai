import numpy as np
from ai.flappybird_env import FlappyBirdEnv
from ai.dqn_agent import DQNAgent
import pygame

def train(episodes=500):
    env = FlappyBirdEnv()
    state_size = 5
    action_size = 2
    agent = DQNAgent(state_size, action_size)

    # Initialize Pygame display for the env (if not already done inside env)
    pygame.init()
    screen = pygame.display.set_mode((288, 512))
    pygame.display.set_caption("Flappy Bird AI Training")

    for e in range(episodes):
        state = np.array(env.reset(), dtype=np.float32)
        total_reward = 0
        done = False
        step = 0

        while not done:
            # Handle Pygame events to keep the window responsive
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            env.render()  # Render the current game state

            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            next_state = np.array(next_state, dtype=np.float32)
            agent.remember(state, action, reward, next_state, done)
            agent.replay()
            state = next_state
            total_reward += reward
            step += 1

            pygame.time.delay(15)  # Small delay to make the game visible

            if done:
                agent.update_target_model()
                print(f"Episode {e+1}/{episodes} | Score: {env.game.current_score} | Reward: {total_reward:.2f} | Epsilon: {agent.epsilon:.2f} | Steps: {step}")
                break

    env.close()
    pygame.quit()

if __name__ == "__main__":
    train(episodes=500)
