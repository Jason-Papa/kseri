import random
from abc import abstractmethod
from collections import Counter


suits= ["♠", "♥", "♦", "♣"]
figures = ["J","Q","K","A"]
numbers = [str(i) for i in range(2,11)] + figures
deck = [number+suit for suit in suits for number in numbers]
GOOD_10 = "10♦"
GOOD_2 = "2♣"

def is_figure(card):
    return card[0] in figures

class Player():
    def __init__(self, name) -> None:
        self.mpaza = []
        self.name = name
        self.hand = []
        self.points = 0
    def add_to_mpaza(self, current_stack):
        self.mpaza += [card for card in current_stack]
    def count_points(self):    
        for card in self.mpaza:
            if is_figure(card) or card == GOOD_10 or card == GOOD_2:
                self.points += 1
        return self.points
    def get_card(self, card):
        self.hand.append(card)

    def add_kseri(self, stack):
        self.points += 10
        if stack[0][0] == "J":
            self.points += 10
        self.add_to_mpaza(stack)

    def get_hand(self):
        return self.hand
        
    @abstractmethod
    def play_card(self, stack, passed_cards):
        pass 
    
class Human(Player):
    def play_card(self, stack, passed_cards):
        for i, card in enumerate(self.hand):
            print(f"{i+1}: {card}")
        card_selection = int(input("Which card would you like to play: ")) - 1
        return self.hand.pop(card_selection)
class Bot(Player):
    def play_card(self, stack, remaining_cards):
        if len(stack):
            top_card = stack[-1][0]
            if any(top_card == hand_card[0] for hand_card in self.hand):
                if ("J"== hand_card[0] for hand_card in self.hand):
                    for i, card in enumerate(self.hand):
                        if card.startswith("J"):
                            return self.hand.pop(i)
                else:
                    for i, card in enumerate(self.hand):
                        if card.startswith(top_card):
                            return self.hand.pop(i)

        occurances_of_numbers_in_passed_cards = Counter([card[0] for card in remaining_cards])
        occurances_of_numbers_in_hand = Counter([card[0] for card in self.hand])
        remaining_occurances = dict(occurances_of_numbers_in_passed_cards - occurances_of_numbers_in_hand)
        best_choice = 0
        smallest_number_of_remaining_cards = 5 # has to be greater than 4
        for i, card in enumerate(self.hand):
            if remaining_occurances[card[0]] < smallest_number_of_remaining_cards:
                smallest_number_of_remaining_cards = remaining_occurances[card[0]]
                best_choice = i
        return self.hand.pop(best_choice)
        

class Game():
    def __init__(self, number_of_players) -> None:
        self.deck = deck
        random.shuffle(self.deck)
        self.stack = self.deck[:4]
        self.deck = self.deck[4:]
        self.players = [Human("Iasonas"),] + [Bot("Bot " + str(player_number)) for player_number in range(number_of_players)]
        self.last_taken = self.players[0]
    
    def get_random_card(self):
        return self.deck.pop(0)
        
    def update(self, player: Player):
        if len(self.stack) == 1:
            return
        if len(self.stack) == 2:
            if self.stack[-2][0] == self.stack[-1][0]:
                player.add_kseri(self.stack)
                self.stack = []
                self.last_taken = player
                return
        if self.stack[-2][0] == self.stack[-1][0] or self.stack[-1][0] == "J":
            player.add_to_mpaza(self.stack)
            self.stack = []
            self.last_taken = player 

    def round(self):
        if len(self.players[0].hand) == 0:
            self.deal()
        for card in self.stack:
            print(card)
        for i, player in enumerate(self.players):
            all_unknown_cards = self.deck
            for j, player_ in enumerate(self.players):
                if i != j:
                    all_unknown_cards += player_.get_hand()
            print(all_unknown_cards, len(all_unknown_cards))
            self.stack.append(player.play_card(self.stack, all_unknown_cards))
            self.update(player)
    
    def deal(self):
        for _ in range(6):
            for player in self.players:
                if self.deck == []:
                    return
                player.get_card(self.deck.pop(0))

    def is_game_over(self):
        return len(self.deck) == 0 and all(player.hand == [] for player in self.players)

    def play(self):
        self.deal()
        while not self.is_game_over():
            self.round() 
        self.last_taken.add_to_mpaza(self.stack)
        self.stack = []  
        max(self.players, key = lambda player: len(player.mpaza)).points += 3
        winner = max(self.players, key= lambda player: player.count_points())
        print(f"Winner: {winner.name} with {winner.points} points!")


            


if __name__=="__main__":
    game = Game(1)
    game.play()