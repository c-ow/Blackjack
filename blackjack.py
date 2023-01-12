import random, math

class Card():
    def __init__(self, num, suit, value):
        self.num = num
        self.suit = suit
        self.value = value
    def __repr__(self):
        return '%s of %s' % (str(self.num), self.suit)

class Ace(Card):
    def __init__(self, num, suit, value):
        self.num = num
        self.suit = suit
        self.value = value
        
class Deck():
    card_deck = []
    def __init__(self):
        self.card_deck = self.shuffle()
    def draw_card(self, player):
        global reshuffle
        if self.card_deck[-1] == 'Plastic Card':
            self.card_deck.remove(self.card_deck[-1])
            reshuffle = True
        player.cards.append(self.card_deck[-1])
        for card in player.cards:
            if isinstance(card, Ace) and player.check_value() > 21:
                if card.value == 11:
                    card.value = 1
        player.check_value()
        self.card_deck.remove(self.card_deck[-1])
    def shuffle(self):
        new_deck = []
        print('\nShuffling deck. . . .\n')
        new_deck.clear()
        for suit in suits:
            new_deck.append(Ace('Ace', suit, 11))
            for i in range(2, 11):
                new_deck.append(Card(i, suit, i))
            for face in faces:
                new_deck.append(Card(face, suit, 10))
        random.shuffle(new_deck)
        new_deck.insert(len(new_deck)-(len(new_deck)//3), 'Plastic Card')
        return new_deck

class Hand():
    def __init__(self, player, cards, value):
        self.player = player
        self.cards = cards
        self.value = value
    def check_value(self):
        self.value = 0
        for card in self.cards:
            self.value += card.value
        return self.value
    def print_hand(self):
        if any(isinstance(card, Ace) and card.value == 11 for card in self.cards):
            alt_value = self.value-10
            print('%s hand: %s : %s/%s' %(self.player, self.cards, self.value, alt_value))
        else:
            print('%s hand: %s : %s' %(self.player, self.cards, self.value))
    def reset_hand(self):
        self.cards.clear()
        self.value = 0

suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
faces = ['Jack', 'Queen', 'King']

dealers_hand, players_hand = Hand('Dealer', [], 0), Hand('Player', [], 0)
split_hand = []
players_money = 100
reshuffle, round_ongoing, new_round = False, False, True

def split(wager):
    if players_hand.cards[0].num == players_hand.cards[1].num:
        dealers_hand.print_hand()
        players_hand.print_hand()
        ask_split = input('Would you like to split your hand? ')
        if ask_split.lower() == 'yes':
            split_wager = input('\nBetting amount for split hand? ')
            if split_wager.isnumeric():
                split_wager = int(split_wager)
                if players_money >= wager+split_wager:
                    split_hand.append(players_hand.cards[1])
                    players_hand.cards.remove(players_hand.cards[1])
                    return split_wager
                else:
                    print('\nYou do not have enough money.\n')
                    split(wager)
        elif ask_split.lower() == 'no':
            pass
        else:
            print('Could not read input')
            split(wager)

def compare_hands(choice):
    if players_hand.value > 21 or dealers_hand.value == 21:
        return 'lost'
    elif players_hand.value == 21 and dealers_hand.value != 21 or dealers_hand.value > 21:
        return 'won'
    if dealers_hand.value >= 17 and choice == 'stand':
        if players_hand.value > dealers_hand.value and players_hand.value <= 21:
            return 'won'
        elif players_hand.value < dealers_hand.value and dealers_hand.value <= 21:
            return 'lost'
        elif players_hand.value == dealers_hand.value or dealers_hand.value == 22: 
            return 'tied'
    
def gameplay(choice):
    if choice == 'hit' or choice == 'double':
        card_deck.draw_card(players_hand)
        if dealers_hand.value < 17:
            card_deck.draw_card(dealers_hand)
    elif choice == 'stand':
        while dealers_hand.value < 17:
            card_deck.draw_card(dealers_hand)
    else:
        print('Could not read input.\n')
    if isinstance(compare_hands(choice), str):
        return compare_hands(choice)

card_deck = Deck()
while True:
    if new_round == True:
        wager = input('Your money : %s\nBetting amount? ' %(players_money))
        if wager.isnumeric():
            wager = int(wager)
            if wager <= players_money: 
                for i in range(2):
                    card_deck.draw_card(dealers_hand)
                    card_deck.draw_card(players_hand)
                split_wager = split(wager)
                new_round = False
                round_ongoing = True
                if dealers_hand.value == 21 or players_hand.value == 21:
                    dealers_hand.print_hand()
                    players_hand.print_hand()
                    round_ongoing = False
                    if players_hand.value == 21 and dealers_hand.value != 21:
                        check = 'won'
                        wager = math.ceil(wager*1.5)
                        print('You got a blackjack!')
                    elif dealers_hand.value == 21 and players_hand.value != 21:
                        check = 'lost'
                        print('The dealer got a blackjack!')
                    elif dealers_hand.value == 21 and players_hand.value == 21:
                        print('Round ended in a tie!')
            else: 
                print('You do not have enough money!')
                continue
        else:
            print('Could not read input. ')
            continue
    while round_ongoing:
        players_hand.check_value()
        dealers_hand.print_hand()
        players_hand.print_hand()
        choice = input('\nHit, stand, double, or surrender? ')
        if choice.lower() == 'double' and wager*2 <= players_money:
            wager += wager
        elif choice.lower() == 'double' and wager*2 > players_money:
            print('\nYou do not have enough money to double.\n')
            continue
        check = gameplay(choice.lower())
        if check == 'lost' or check == 'won' or check == 'tied': 
            dealers_hand.print_hand()
            players_hand.print_hand()
            round_ongoing = False
    print('\nYou %s the round.\n' % (check))
    if check == 'tied':
        wager = 0
    players_money = players_money - wager if check == 'lost' else players_money + wager
    players_hand.reset_hand()
    dealers_hand.reset_hand()
    if len(split_hand) > 0:
        for i in range(2):
            card_deck.draw_card(dealers_hand)
        players_hand.cards.append(split_hand[0])
        players_hand.value = split_hand[0].value
        split_hand.clear()
        wager = split_wager
        print('Your money : %s' %(players_money))
        round_ongoing = True
        continue
    elif len(split_hand) == 0:
        print('Your money : %s' %(players_money))
        if players_money <= 0:
            print('You ran out of money.')
            break
        play_again = input('Play another round? ')
        if play_again.lower() == 'yes' or play_again.lower() == 'y' and players_money > 0:
            if reshuffle == True:
                card_deck = Deck()
                reshuffle = False
            new_round = True
            continue
        elif play_again.lower() == 'no' or play_again.lower() == 'n':
            print('Thank you for playing!')
            break
        else:
            print('Could not read input.')
            continue