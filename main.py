import random
#

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]



def calculate_score(deck):
    """Takes a list of cards and returns the score calculated from them"""

    if sum(deck) == 21 and len(deck) == 2:
        return 21

    if 11 in deck  and sum(deck) > 21:
        deck.remove(11)
        deck.append(1)
        return sum(deck)

    else:
        return sum(deck)



#comuters_score= sum(computer_cards)
def deal_cards(players_cards):
    card = random.choice(cards)
    players_cards.append(card)


def display_cards(players_cards,opponent_cards):
    print(f"Your cards:{players_cards}, current score: {calculate_score(players_cards)}")
    print(f"computers first hand :{opponent_cards[0]}")






def decide_winner(players_cards, opponents_cards):
    player_score = calculate_score(players_cards)
    opponent_score = calculate_score(opponents_cards)
    # Both bust - no winner (or house wins)
    if player_score > 21 and opponent_score > 21:
            print("tie")   # or "house wins"

        # Player busts, opponent doesn't
    if player_score > 21 and opponent_score <= 21:
        print(f"\nYOU LOSE \n\n\n your final hand is :{players_cards} final score= {calculate_score(players_cards)}")
        print(f"computers final hand:{opponents_cards} final score = {calculate_score(opponents_cards)}")

        # Opponent busts, player doesn't
    if opponent_score > 21  and player_score <= 21:
        print(f"\nYOU WIN \n\nyour final hand is :{players_cards} final score= {calculate_score(players_cards)}")
        print(f"computers final hand:{opponents_cards} final score = {calculate_score(opponents_cards)}")

def decide_winner_when_the_two_layers_are_under_21(players_cards,opponents_cards):   # Both under 21 - closest to 21 wins
    player_score = calculate_score(players_cards)
    opponent_score = calculate_score(opponents_cards)

    if player_score < 21 and opponent_score < 21:
        if player_score > opponent_score:
            print(f"\nYOU WIN \n\nyour final hand is :{players_cards} final score= {calculate_score(players_cards)}")
            print(f"computers final hand:{opponents_cards} final score = {calculate_score(opponents_cards)}")

        elif opponent_score > player_score:
            print(f"\nYOU LOSE \n\nyour final hand is :{players_cards} final score= {calculate_score(players_cards)}")
            print(f"computers final hand:{opponents_cards} final score = {calculate_score(opponents_cards)}")
    else:
        pass




def game():
    user_cards = []

    computer_cards = []

    playing = True
    while playing:
        for _ in range (2):
            deal_cards(user_cards)
            deal_cards(computer_cards)

        display_cards(user_cards,computer_cards)

        if calculate_score(user_cards) == 21 or calculate_score(computer_cards) == 21 or calculate_score(user_cards) > 21:
            playing = False

        else:
            user_choice = input("if you want to get another card type 'y' else type 'n' ")
            if user_choice == "y":
                deal_cards(user_cards)

                display_cards(user_cards,opponent_cards=computer_cards)
                decide_winner(user_cards, computer_cards)
                decide_winner_when_the_two_layers_are_under_21(user_cards, computer_cards)


            elif user_choice == "n":
                display_cards(user_cards, opponent_cards=computer_cards)
                decide_winner(user_cards,computer_cards)
                decide_winner_when_the_two_layers_are_under_21(user_cards, computer_cards)
            else:
                pass



            play_again= input("do you want to lay a game of blackjack tye 'y' or 'n' \n")
            if play_again == "y":
                print("\n" * 50)
                game()
            else:
                playing= False
game()

#Card games with known probability spaces
#Turn-based strategy where you need to evaluate moves ahead
#Debugging complex state systems where you need to trace specific edge cases


