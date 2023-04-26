# splendor.py
import random

import pandas as pd

from game_components import Card, Noble, Token, Player, LinkedListNode, COLOR
import numpy as np

class Splendor:
    def __init__(self, players):
        self.players = players
        random.shuffle(self.players)
        self.num_player = len(self.players)

        self.level1_card, self.level2_card, self.level3_card = self.generate_cards()
        self.nobles = self.generate_nobles()
        self.tokens = self.generate_tokens()

        self.public_cards_level1 = []
        self.public_cards_level2 = []
        self.public_cards_level3 = []
        self.generate_public_cards()

        self.current_player = self.players[0]
        self.turn_count = 0
        self.game_end_triggered = False

    def generate_public_cards(self):
        for i in range(4):
            self.public_cards_level1.append(self.level1_card.pop())
            self.public_cards_level2.append(self.level2_card.pop())
            self.public_cards_level3.append(self.level3_card.pop())

        assert len(self.public_cards_level1) == 4
        assert len(self.public_cards_level2) == 4
        assert len(self.public_cards_level3) == 4
        assert self.level1_card.length() == 36
        assert self.level2_card.length() == 26
        assert self.level3_card.length() == 16

    def is_game_over(self):
        current_player = self.players[self.turn_count % len(self.players)]

        if current_player.points >= 15:
            self.game_end_triggered = True

        if self.game_end_triggered:
            if self.turn_count % len(self.players) == len(self.players) - 1:
                return True

        return False

    def determine_winner(self):
        max_points = max(player.points for player in self.players)
        potential_winners = [player for player in self.players if player.points == max_points]

        if len(potential_winners) == 1:
            return potential_winners[0]
        else:
            # In case of a tie, the player who has purchased the fewest development cards wins
            # if there are multiple winners still, the one who started later wins.
            fewest_development_cards = min(len(player.owned_cards) for player in potential_winners)
            winner = [player for player in potential_winners if len(player.owned_cards) == fewest_development_cards][-1]
            return winner

    def generate_cards(self):
        df = pd.read_csv('cards.csv')
        level1_card = df[df.level == 1]
        dummy_node_level1 = LinkedListNode(card=None)
        cur_node = dummy_node_level1
        for _, row in level1_card.iterrows():
            card = Card(card_id=row['id'], level=1, points=row['point'], color='color', cost={key: row[key] for key in ['white', 'blue', 'green', 'red', 'black']})
            node = LinkedListNode(card=card)
            cur_node.next_node = node
            cur_node = cur_node.next_node

        level1_card = dummy_node_level1.next_node.shuffle()

        level2_card = df[df.level == 2]
        dummy_node_level2 = LinkedListNode(card=None)
        cur_node = dummy_node_level2
        for _, row in level2_card.iterrows():
            card = Card(card_id=row['id'], level=2, points=row['point'], color='color',
                        cost={key: row[key] for key in ['white', 'blue', 'green', 'red', 'black']})
            node = LinkedListNode(card=card)
            cur_node.next_node = node
            cur_node = cur_node.next_node

        level2_card = dummy_node_level2.next_node.shuffle()

        level3_card = df[df.level == 3]
        dummy_node_level3 = LinkedListNode(card=None)
        cur_node = dummy_node_level3
        for _, row in level3_card.iterrows():
            card = Card(card_id=row['id'], level=3, points=row['point'], color='color',
                        cost={key: row[key] for key in ['white', 'blue', 'green', 'red', 'black']})
            node = LinkedListNode(card=card)
            cur_node.next_node = node
            cur_node = cur_node.next_node

        level3_card = dummy_node_level3.next_node.shuffle()

        assert level1_card.length() == 40
        assert level2_card.length() == 30
        assert level3_card.length() == 20
        return level1_card, level2_card, level3_card

    def generate_nobles(self):
        df = pd.read_csv('nobles.csv')
        noble_list = []
        for _, row in df.iterrows():
            noble = Noble(requirements={key: row[key] for key in ['white', 'blue', 'green', 'red', 'black']},
                          points=3)
            noble_list.append(noble)
        random.shuffle(noble_list)
        assert len(noble_list) == 10
        return noble_list[:(self.num_player + 1)]

    def generate_tokens(self):
        num_token = 4 if self.num_player == 2 else 5 if self.num_player == 3 else 7
        tokens = {color: num_token for color in COLOR}
        tokens['gold'] = 5
        return tokens

    def buy_card(self, player, card):
        # Check if the player can afford the card
        # TODO：更新
        can_afford = self.can_afford(player, card)

        if can_afford:
            # Remove the card cost from the player's tokens
            for color, cost in card.cost.items():
                for _ in range(cost):
                    player.tokens.remove(color)

            # Add the card to the player's cards and increase their points
            player.cards.append(card)
            player.points += card.points

            # Remove the card from the available cards
            self.cards.remove(card)

    def can_afford(self, player, card):
        gap = 0
        for color in COLOR:
            color_gap = card.cost[color] > player.tokens[color] + player.owned_cards[color]
            if color_gap > 0:
                gap += color_gap
        if gap > player.tokens['gold']:
            return False
        return True

    def reserve_card(self, player, card):
        if len(player.reserved_cards) < 3:
            player.reserved_cards.append(card)
            self.cards.remove(card)

    def take_tokens(self, player, tokens):
        if len(player.tokens) + len(tokens) <= 10:
            for token in tokens:
                if self.tokens.count(token) > 0:
                    player.tokens.append(token)
                    self.tokens.remove(token)

    # Add this method to the Splendor class in splendor.py

    def player_turn(self, player):
        print(f"{player.name}'s turn:")
        print("1. Buy a card")
        print("2. Reserve a card")
        print("3. Take tokens")

        choice = int(input("Enter the number of your choice: "))
        if choice == 1:
            card_index = int(input("Enter the index of the card you want to buy: "))
            card = self.cards[card_index]
            self.buy_card(player, card)
        elif choice == 2:
            card_index = int(input("Enter the index of the card you want to reserve: "))
            card = self.cards[card_index]
            self.reserve_card(player, card)
        elif choice == 3:
            token_count = int(input("Enter the number of tokens you want to take: "))
            tokens = []
            for _ in range(token_count):
                token_color = input("Enter the color of the token: ")
                tokens.append(Token(token_color))
            self.take_tokens(player, tokens)
        else:
            print("Invalid choice.")

    def reset(self):
        # Reset cards on the board
        self.cards = self.generate_cards()

        # Reset player states
        for player in self.players:
            player.reset()

    def perform_action(self, player, action):
        # Perform the chosen action in the game environment
        if action == 0:
            # Buy a card
            card_index = np.random.randint(len(self.cards))  # Example: Randomly choose a card to buy
            card = self.cards.pop(card_index)
            player.owned_cards.append(card)
            player.points += card.points
        elif action == 1:
            # Reserve a card
            card_index = np.random.randint(len(self.cards))  # Example: Randomly choose a card to reserve
            card = self.cards.pop(card_index)
            player.reserved_cards.append(card)
        elif action == 2:
            # Take tokens
            token_index = np.random.randint(len(player.tokens))  # Example: Randomly choose a token type to take
            player.tokens[token_index] += 1

        # Calculate the reward for the action
        reward = self.calculate_reward(player, action)

        # Check if the game has ended
        done = self.is_game_over()

        # Get the next state
        next_state = self.state_to_array()

        return next_state, reward, done

    def calculate_reward(self, player, action):
        # Calculate the reward for the chosen action
        reward = 0

        # Add heuristic score to guide exploration
        # heuristic_score = self.heuristic_score(player)
        # reward += heuristic_score

        # Check if the game has ended and assign rewards/penalties
        if self.is_game_over():
            if player.points >= 15:
                reward += 100  # Reward

    def state_to_array(self):
        # Convert the game state into a suitable format for the agent
        # This is just an example; you'll need to customize this function for your use case
        state = np.zeros(10)  # Example: 10-dimensional state
        return np.reshape(state, [1, -1])
