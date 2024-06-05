def generate_deck():
    """Generate a standard deck of playing cards."""
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['h', 'd', 'c', 's']
    deck = [(rank, suit) for rank in ranks for suit in suits]
    return deck


def generate_combinations(deck):
    """Generate all possible two-card combinations."""
    return [(card1, card2) for i, card1 in enumerate(deck) for card2 in deck[i + 1:]]


def display_combinations(combinations):
    """Display the combinations in a table format."""
    print("Two-Card Combinations:")
    print("----------------------")
    for i, (card1, card2) in enumerate(combinations, start=1):
        print(f"{i}. {card1[0]} of {card1[1]} and {card2[0]} of {card2[1]}")


if __name__ == "__main__":
    deck_of_cards = generate_deck()
    all_combinations = generate_combinations(deck_of_cards)
    display_combinations(all_combinations)
    print("Generated " + all_combinations.count() + " combinations.")