import random
import os
import copy


class Card:
    def __init__(self, value: int, suit: str):
        self.value = value
        self.suit = suit

    def __lt__(self, other):
        t1 = self.suit, self.value
        t2 = other.suit, other.value
        return t1 < t2

    def __str__(self):
        if self.value > 10:
            if self.value == 11:
                return "| {} {} |".format("J", self.suit)
            elif self.value == 12:
                return "| {} {} |".format("Q", self.suit)
            elif self.value == 13:
                return "| {} {} |".format("K", self.suit)
            elif self.value == 14:
                return "| {} {} |".format("A", self.suit)
        else:
            return f"| {self.value} {self.suit} |"


class Deck:
    def __init__(self, deck_type: int):
        self.deck_type = deck_type
        self.deck = []

    def build_deck(self):
        if self.deck_type == 36:
            lowest_value = 6
        elif self.deck_type == 52:
            lowest_value = 2
        for suit in ["♠", "♥", "♦", "♣"]:
            for value in range(lowest_value, 15):
                self.deck.append(Card(value, suit))

    def display_deck(self):
        for card in self.deck:
            print(card, end="")

    def shuffle(self):  # Fisher–Yates shuffle Algorithm
        for i in range(len(self.deck) - 1, 0, -1):
            random_index = random.randint(0, i)
            self.deck[i], self.deck[random_index] = self.deck[random_index], self.deck[i]
        global dc
        dc = copy.deepcopy(self.deck[0])

    def pop_card(self):
        if self.deck:
            return self.deck.pop()

    @staticmethod
    def trump_card():
        return dc


class Player:
    def __init__(self):
        self.hand = []
        self.turn = None
        self.took = False

    def take_card(self, deck):
        self.hand.append(deck.pop_card())

    def sort_hand(self):
        self.hand.sort()

    def display_hand(self):
        for card in self.hand:
            print(card, end="")

    def make_move(self, game):
        while True:
            try:
                index = int(input("Your move, please write index of card: "))
            except ValueError:
                print("Type only positive number of a card. Indexing goes from left to right")
            else:
                print("Nice!")
                break
        game.board.append([self.hand.pop(index - 1), None])

    def beat_card(self, game, deck):  # TODO: change names of variables
        result = False
        while result is not True:
            index_hand = input("""Please write index of card or "Take": """)
            if isinstance(index_hand, str):
                if index_hand == "Take":
                    for turn in game.board:  # TODO: check for two variables instead of nested loop
                        for card in turn:
                            if card is not None:
                                self.hand.append(card)
                    game.board.clear()
                    result = True
                    self.took = True
                    break
            try:
                index_hand = int(index_hand) - 1  # Get reed of human readable indexing
            except ValueError:
                print("Take without quotations and capitalized")
                continue
            for index, turn in enumerate(game.board):
                if turn[1] is None:
                    if self.hand[index_hand].suit == turn[0].suit:
                        if self.hand[index_hand].value > turn[0].value:
                            game.board[index][1] = self.hand.pop(index_hand)
                            result = True
                            self.took = False
                            break
                    elif self.hand[index_hand].suit == deck.trump_card().suit and turn[
                        0].suit != deck.trump_card().suit:
                        game.board[index][1] = self.hand.pop(index_hand)
                        result = True
                        self.took = False
                        break


class Computer(Player):
    def __init__(self):
        super().__init__()

    def make_move(self, game, deck):  # TODO: Throws trumps
        lowest_card = self.hand[0]
        for card in self.hand:
            if card.value < lowest_card.value and card.suit != deck.trump_card():
                lowest_card = card
        game.board.append([self.hand.pop(self.hand.index(lowest_card)), None])

    def beat_card(self, game, deck):
        for index, turn in enumerate(game.board):
            if turn[1] is None:
                result = False
                for card in self.hand:
                    if card.suit == turn[0].suit and card.value > turn[0].value:
                        game.board[index][1] = self.hand.pop(self.hand.index(card))
                        result = True
                        self.took = False
                        break
                if not result:
                    for card in self.hand:
                        if card.suit == deck.trump_card().suit:
                            game.board[index][1] = self.hand.pop(self.hand.index(card))
                            result = True
                            self.took = False
                            break
        if not result:
            for turn in game.board:  # TODO: check for two variables instead of nested loop
                for card in turn:
                    if card is not None:
                        self.hand.append(card)
            self.took = True
            game.board.clear()


class Game:
    def __init__(self):
        self.board = []
        self.p1_trumps = []
        self.c1_trumps = []

    @staticmethod
    def start(deck, player, computer):
        for i in range(6):
            computer.take_card(deck)
            player.take_card(deck)

    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    def first_move(self, deck, player, computer):
        lowest_trump = 0
        for card in player.hand:
            if card.suit == deck.trump_card().suit:
                self.p1_trumps.append(card.value)
        for card in computer.hand:
            if card.suit == deck.trump_card().suit:
                self.c1_trumps.append(card.value)
        if not self.p1_trumps or not self.c1_trumps:
            if not self.c1_trumps and not self.p1_trumps:
                if random.randint(1, 10) % 2 == 0:
                    player.turn = True
                    computer.turn = False
                else:
                    player.turn = False
                    computer.turn = True
            elif not self.p1_trumps:
                player.turn = False
                computer.turn = True
            else:
                player.turn = True
                computer.turn = False
        else:
            lowest_trump = min(min(self.p1_trumps), min(self.c1_trumps))
        if lowest_trump in self.p1_trumps:
            player.turn = True
            computer.turn = False
        else:
            player.turn = False
            computer.turn = True

    def display_game(self, computer, player, deck):
        print("Computer: ", end="")
        print("| # |"*len(computer.hand))
        print()
        print()
        print("Trump card      Board")
        print(deck.trump_card(), end="")
        print("        ", end="")
        if computer.turn == True:
            print(self.board[0][0], end="")
            print()
            print()
            print("Player: ", end="")
            player.display_hand()
            print()
        else:
            print()
            print()
            print("Player: ", end="")
            player.display_hand()
            print()

if __name__ == "__main__":
    deck_type = input("Do you want 36 or 52 cards?: ")
    while True:
        if deck_type == "36":
            deck1 = Deck(36)
            break
        elif deck_type == "52":
            deck1 = Deck(52)
            break
        else:
            print("Wrong input, type just a number")
    game1 = Game()
    player1 = Player()
    computer1 = Computer()
    deck1.build_deck()
    deck1.shuffle()
    game1.start(deck1, player1, computer1)
    computer1.sort_hand()
    player1.sort_hand()
    game1.first_move(deck1, player1, computer1)
    game1.clear_console()

    while True:
        if not deck1.deck and not player1.hand:
            print("YOU ARE THE CHAMPION")
            break
        elif not deck1.deck and not computer1.hand:
            print("LOSE")
            break

        if player1.turn:
            game1.display_game(computer1, player1, deck1)
            player1.make_move(game1)
            computer1.beat_card(game1, deck1)
            if computer1.took == False:
                player1.turn = False
                computer1.turn = True
            else:
                player1.turn = True
                computer1.turn = False
            player1.take_card(deck1)
            if player1.hand[-1] is None: player1.hand.pop()
            player1.sort_hand()
            game1.board.clear()
            game1.clear_console()
            if len(computer1.hand) < 6:
                computer1.take_card(deck1)
                if computer1.hand[-1] is None: computer1.hand.pop()
                computer1.sort_hand()

        elif computer1.turn:
            computer1.make_move(game1, deck1)
            game1.display_game(computer1, player1, deck1)
            player1.beat_card(game1, deck1)
            if player1.took == False:
                player1.turn = True
                computer1.turn = False
            else:
                player1.turn = False
                computer1.turn = True
            computer1.take_card(deck1)
            if computer1.hand[-1] is None: computer1.hand.pop()
            computer1.sort_hand()
            game1.board.clear()
            game1.clear_console()
            if len(player1.hand) < 6:
                player1.take_card(deck1)
                if player1.hand[-1] is None: player1.hand.pop()
                player1.sort_hand()
