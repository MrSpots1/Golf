import unittest

from CardDeck import CardDeck
from Card import Card
from CardSuit import CardSuit
from CardType import CardType


class TestCardDeck(unittest.TestCase):
    def test_init_invalid_deck_count_raises_value_error(self):
        with self.assertRaises(ValueError):
            CardDeck(0)

    def test_initial_deck_size_single_deck(self):
        deck = CardDeck(1)
        expected = len(list(CardSuit)) * len(list(CardType))
        self.assertEqual(deck.cards_left(), expected)

    def test_initial_deck_size_multi_deck(self):
        deck = CardDeck(2)
        expected = 2 * len(list(CardSuit)) * len(list(CardType))
        self.assertEqual(deck.cards_left(), expected)

    def test_draw_card_reduces_count_and_returns_card(self):
        deck = CardDeck(1)
        start = deck.cards_left()
        card = deck.draw_card()
        self.assertIsInstance(card, Card)
        self.assertEqual(deck.cards_left(), start - 1)

    def test_draw_card_from_empty_raises_index_error(self):
        deck = CardDeck(1)
        # Exhaust the deck
        while deck.cards_left() > 0:
            deck.draw_card()
        # Drawing from empty deck should raise IndexError
        with self.assertRaises(IndexError):
            deck.draw_card()

    def test_discard_and_top_discard(self):
        deck = CardDeck(1)
        card = deck.draw_card()
        deck.discard(card)
        self.assertEqual(deck.topDiscardCard(), card)

    def test_top_discard_raises_on_empty(self):
        deck = CardDeck(1)
        with self.assertRaises(Exception):
            deck.topDiscardCard()

    def test_take_discard_card_returns_and_removes(self):
        deck = CardDeck(1)
        card = deck.draw_card()
        deck.discard(card)
        taken = deck.takeDiscardCard()
        self.assertEqual(taken, card)
        self.assertEqual(len(deck.discards), 0)

    def test_take_discard_card_raises_on_empty(self):
        deck = CardDeck(1)
        with self.assertRaises(Exception):
            deck.takeDiscardCard()

    def test_discards_to_cards_moves_when_draw_pile_empty(self):
        deck = CardDeck(1)
        # Draw all cards to empty the draw pile
        drawn = []
        while deck.cards_left() > 0:
            drawn.append(deck.draw_card())
        # Put a few cards onto the discard pile
        for i in range(5):
            deck.discard(drawn[i])
        self.assertEqual(len(deck.discards), 5)
        # Move discards back to cards and shuffle
        deck.discards_to_cards()
        self.assertEqual(deck.cards_left(), 5)
        self.assertEqual(len(deck.discards), 0)

    def test_discards_to_cards_raises_when_draw_pile_not_empty(self):
        deck = CardDeck(1)
        # Ensure there is at least one card in the draw pile
        self.assertGreater(deck.cards_left(), 0)
        # Add a card to the discard pile
        deck.discard(Card(CardSuit.Heart, CardType.Ace))
        with self.assertRaises(Exception):
            deck.discards_to_cards()

    def test_shuffle_keeps_count_same(self):
        deck = CardDeck(1)
        before = deck.cards_left()
        deck.shuffle()
        self.assertEqual(deck.cards_left(), before)


if __name__ == "__main__":
    unittest.main()
