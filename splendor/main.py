import pygame
import numpy as np
import sys
import argparse
from splendor import Splendor, Player
from DQNAgent import DQNAgent


def parse_args():
    parser = argparse.ArgumentParser(description="Splendor game with DQN agent")
    parser.add_argument("--mode", type=str, default="interactive", choices=["interactive", "training"], help="Choose game mode (interactive or training)")
    return parser.parse_args()


def save_agent(agent, filename):
    agent.save_model(filename)


def load_agent(agent, filename):
    agent.load_model(filename)


def average_weights(agent1, agent2):
    weights1 = agent1.model.get_weights()
    weights2 = agent2.model.get_weights()

    averaged_weights = [(w1 + w2) / 2 for w1, w2 in zip(weights1, weights2)]
    return averaged_weights


def main(args):
    # Initialize pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Splendor")

    if args.mode == "interactive":
        player1 = Player("Player 1")
        player2 = DQNAgent("Player 2", state_size=10, action_size=3, learning_rate=0.001, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995)
        game = Splendor([player1, player2])
        load_agent(player2, "trained_agent.h5")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw game state
            for player in game.players:
                player.draw(screen, game.cards)

            # Update the display
            pygame.display.flip()

        pygame.quit()

    elif args.mode == "training":
        player1 = DQNAgent("Player 1", state_size=10, action_size=3, learning_rate=0.001, discount_factor=0.99,
                           exploration_rate=1.0, exploration_decay=0.995)
        player2 = DQNAgent("Player 2", state_size=10, action_size=3, learning_rate=0.001, discount_factor=0.99,
                           exploration_rate=1.0, exploration_decay=0.995)
        combined_agent = DQNAgent("Combined Agent", state_size=10, action_size=3, learning_rate=0.001,
                                  discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995)
        game = Splendor([player1, player2])

        num_episodes = 1000
        for episode in range(num_episodes):
            game.reset()
            done = False

            while not done:
                # Agent chooses action
                state = game.state_to_array()

                action = player1.choose_action(state)

                # Perform action and get new state, reward, and done flag
                next_state, reward, done = game.perform_action(player1, action)

                # Agent learns from experience
                player1.remember(state, action, reward, next_state, done)
                player1.replay()

                # Update the state and exploration rate
                state = next_state
                player1.update_exploration_rate()

                action = player2.choose_action(state)

                # Perform action and get new state, reward, and done flag
                next_state, reward, done = game.perform_action(player2, action)

                # Agent learns from experience
                player2.remember(state, action, reward, next_state, done)
                player2.replay()

                # Update the state and exploration rate
                state = next_state
                player2.update_exploration_rate()

                game.turn_count += 1

                if game.is_game_over():
                    winner = game.determine_winner()
                    print("Winner:", winner.name)
                    break

        averaged_weights = average_weights(player1, player2)

        combined_agent.model.set_weights(averaged_weights)

        # Save the trained agent
        save_agent(player2, "trained_agent.h5")



if __name__ == "__main__":
    args = parse_args()
    main(args)