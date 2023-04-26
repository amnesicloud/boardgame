# game_components.py

# class Card:
#     def __init__(self, level, points, cost):
#         self.level = level
#         self.points = points
#         self.cost = cost
import random

COLOR = ['white', 'blue', 'green', 'red', 'black']
class Card:
    def __init__(self, card_id, level, points, color, cost):
        self.card_id = card_id
        self.level = level
        self.points = points
        self.color = color
        self.cost = cost  # Add the cost attribute as a dictionary representing tokens of 5 colors

    def __str__(self):
        return f"Card(id: {self.card_id}, level: {self.level}, points: {self.points}, color: {self.color}, cost: {self.cost})"

class Noble:
    def __init__(self, requirements, points):
        self.requirements = requirements
        self.points = points

class Token:
    def __init__(self, color):
        self.color = color

class Player:
    def __init__(self, name):
        self.name = name
        self.owned_cards = {color: 0 for color in COLOR}
        self.tokens = {color: 0 for color in COLOR}
        self.tokens['gold'] = 0
        self.reserved_cards = []
        self.points = 0

    def reset(self):
        self.points = 0
        self.owned_cards = {color: 0 for color in COLOR}
        self.reserved_cards = []
        self.tokens = {color: 0 for color in COLOR}
        self.tokens['gold'] = 0



class LinkedListNode:
    def __init__(self, card, next_node=None):
        self.card = card
        self.next_node = next_node

    def shuffle(self):
        # Convert the linked list to a list
        node_list = []
        current_node = self
        while current_node is not None:
            node_list.append(current_node)
            current_node = current_node.next_node

        # Shuffle the list
        random.shuffle(node_list)

        # Convert the shuffled list back to a linked list
        for i in range(len(node_list) - 1):
            node_list[i].next_node = node_list[i + 1]
        node_list[-1].next_node = None
        return node_list[0]

    def pop(self):
        if self.next_node is None:
            raise ValueError("Cannot pop from an empty list")

        popped_card = self.next_node.card
        self.next_node = self.next_node.next_node
        return popped_card

    def length(self):
        cur = self
        ret = 1
        while cur.next_node is not None:
            cur = cur.next_node
            ret += 1
        return ret

    def hasNextNode(self):
        if self.next_node is None:
            return False
        return True
