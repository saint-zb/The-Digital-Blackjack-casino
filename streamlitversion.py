import streamlit as st
import random
from art import logo

# Initialize session state
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'user_cards' not in st.session_state:
    st.session_state.user_cards = []
if 'computer_cards' not in st.session_state:
    st.session_state.computer_cards = []
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'show_computer_cards' not in st.session_state:
    st.session_state.show_computer_cards = False

# Card deck
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def calculate_score(deck):
    """Takes a list of cards and returns the score calculated from them"""
    if sum(deck) == 21 and len(deck) == 2:
        return 21

    # Handle Ace conversion (11 to 1)
    deck_copy = deck.copy()  # Don't modify original
    if 11 in deck_copy and sum(deck_copy) > 21:
        deck_copy.remove(11)
        deck_copy.append(1)

    return sum(deck_copy)


def deal_card():
    """Returns a random card from the deck"""
    return random.choice(cards)


def get_card_display(card_value):
    """Convert card value to display string"""
    if card_value == 11:
        return "A"
    elif card_value == 10:
        return random.choice(["10", "J", "Q", "K"])
    else:
        return str(card_value)


def computer_should_hit(computer_cards):
    """Computer hits if score is less than 17"""
    return calculate_score(computer_cards) < 17


def decide_winner(user_cards, computer_cards):
    """Determine and return the winner"""
    user_score = calculate_score(user_cards)
    computer_score = calculate_score(computer_cards)

    # Both bust
    if user_score > 21 and computer_score > 21:
        return "tie", "Both players bust!"

    # User busts
    if user_score > 21:
        return "computer", f"You bust with {user_score}!"

    # Computer busts
    if computer_score > 21:
        return "user", f"Computer busts with {computer_score}!"

    # Both valid scores
    #valid concern
    #if they are both under 21 and the layer doesnt take another card
    #
    #
    #
    if user_score > computer_score:
        return "user", f"You win! {user_score} beats {computer_score}"
    elif computer_score > user_score:
        return "computer", f"Computer wins! {computer_score} beats {user_score}"
    else:
        return "tie", f"It's a tie! Both have {user_score}"


def reset_game():
    """Reset all game variables"""
    st.session_state.user_cards = []
    st.session_state.computer_cards = []
    st.session_state.game_over = False
    st.session_state.show_computer_cards = False
    st.session_state.game_started = False


# Streamlit UI
st.title("🎴 Blackjack Game")
st.code(logo)
st.markdown("---")

# New Game Button
if st.button("🎮 New Game", type="primary") or not st.session_state.game_started:
    if not st.session_state.game_started:
        # Deal initial cards
        st.session_state.user_cards = [deal_card(), deal_card()]
        st.session_state.computer_cards = [deal_card(), deal_card()]
        st.session_state.game_started = True
        st.session_state.game_over = False
        st.session_state.show_computer_cards = False
    else:
        reset_game()
        st.session_state.user_cards = [deal_card(), deal_card()]
        st.session_state.computer_cards = [deal_card(), deal_card()]
        st.session_state.game_started = True

    st.rerun()

if st.session_state.game_started:
    # Display cards and scores
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🙋‍♀️ Your Hand")
        user_score = calculate_score(st.session_state.user_cards)

        # Display user cards
        card_display = " | ".join([get_card_display(card) for card in st.session_state.user_cards])
        st.write(f"**Cards:** {card_display}")
        st.write(f"**Score:** {user_score}")

        # Check for blackjack
        if user_score == 21 and len(st.session_state.user_cards) == 2:
            st.success("🎉 BLACKJACK!")

    with col2:
        st.subheader("🤖 Computer's Hand")
        computer_score = calculate_score(st.session_state.computer_cards)

        if st.session_state.show_computer_cards or st.session_state.game_over:
            # Show all computer cards
            card_display = " | ".join([get_card_display(card) for card in st.session_state.computer_cards])
            st.write(f"**Cards:** {card_display}")
            st.write(f"**Score:** {computer_score}")
        else:
            # Show only first card
            st.write(f"**Cards:** {get_card_display(st.session_state.computer_cards[0])} | ?")
            st.write(f"**Score:** ?")

    st.markdown("---")

    # Game logic
    if not st.session_state.game_over:
        user_score = calculate_score(st.session_state.user_cards)
        computer_score = calculate_score(st.session_state.computer_cards)

        # Check for immediate win conditions
        if user_score == 21 or computer_score == 21 or user_score > 21:
            st.session_state.game_over = True
            st.session_state.show_computer_cards = True
        else:
            # Player's turn
            col1, col2 = st.columns(2)

            with col1:
                if st.button("🎯 Hit (Draw Card)", type="secondary"):
                    st.session_state.user_cards.append(deal_card())
                    user_score = calculate_score(st.session_state.user_cards)

                    if user_score > 21:
                        st.session_state.game_over = True
                        st.session_state.show_computer_cards = True

                    st.rerun()

            with col2:
                if st.button("✋ Stand", type="secondary"):
                    st.session_state.show_computer_cards = True

                    # Computer's turn
                    while computer_should_hit(st.session_state.computer_cards):
                        st.session_state.computer_cards.append(deal_card())

                    st.session_state.game_over = True
                    st.rerun()

    # Show results if game is over
    if st.session_state.game_over:
        st.markdown("---")
        winner, message = decide_winner(st.session_state.user_cards, st.session_state.computer_cards)

        if winner == "user":
            st.success(f"🎉 {message}")
        elif winner == "computer":
            st.error(f"😢 {message}")
        #else:
         #   pass
        #st.info(f"🤝 {message}")

        # Final scores
        st.write("### Final Results")
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Your final score:** {calculate_score(st.session_state.user_cards)}")

        with col2:
            st.write(f"**Computer's final score:** {calculate_score(st.session_state.computer_cards)}")

else:
    st.info("👆 Click 'New Game' to start playing!")

# Sidebar with game rules
st.sidebar.title("📋 Game Rules")
st.sidebar.write("""
**Blackjack Rules:**
- Get as close to 21 as possible without going over
- Face cards (J, Q, K) are worth 10 points
- Aces are worth 11 or 1 (automatically adjusted)
- If you go over 21, you "bust" and lose
- Computer hits until 17 or higher
- Closest to 21 wins!
""")

st.sidebar.title("🎮 How to Play")
st.sidebar.write("""
1. Click **New Game** to start
2. You'll get 2 cards, computer gets 2 cards
3. Click **Hit** to draw another card
4. Click **Stand** when you're satisfied
5. Try to beat the computer's score!

""")
