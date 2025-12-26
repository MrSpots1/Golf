import unittest

from CardSlot import CardSlot
from Card import Card
from CardSuit import CardSuit
from CardType import CardType


class TestCardSlot(unittest.TestCase):
    def test_initial_state(self):
        slot = CardSlot(row=0, column=1)
        self.assertIsNone(slot.card)
        self.assertTrue(slot.isFaceDown)
        self.assertEqual(slot.row, 0)
        self.assertEqual(slot.column, 1)

    def test_place_hidden_card_sets_card_and_face_down(self):
        slot = CardSlot(0, 0)
        card = Card(CardSuit.Heart, CardType.Five)
        slot.placeHiddenCard(card)
        self.assertEqual(slot.card, card)
        self.assertTrue(slot.isFaceDown)
        # display should be hidden
        self.assertEqual(slot.display(), "??")

    def test_place_hidden_card_raises_if_already_has_card(self):
        slot = CardSlot(0, 0)
        first = Card(CardSuit.Club, CardType.Two)
        slot.placeHiddenCard(first)
        with self.assertRaises(ValueError):
            slot.placeHiddenCard(Card(CardSuit.Spade, CardType.Ace))

    def test_reveal_card_changes_state_and_raises_if_already_revealed(self):
        slot = CardSlot(0, 0)
        # reveal with no card present still flips face state per implementation
        slot.revealCard()
        self.assertFalse(slot.isFaceDown)
        # second reveal should raise
        with self.assertRaises(ValueError):
            slot.revealCard()

    def test_place_revealed_card_sets_card_and_face_up(self):
        slot = CardSlot(0, 0)
        card = Card(CardSuit.Diamond, CardType.Queen)
        slot.placeRevealedCard(card)
        self.assertEqual(slot.card, card)
        self.assertFalse(slot.isFaceDown)
        # display should show the card string
        self.assertEqual(slot.display(), card.display())

    def test_place_revealed_overwrites_existing_card(self):
        slot = CardSlot(0, 0)
        slot.placeHiddenCard(Card(CardSuit.Heart, CardType.Nine))
        new_card = Card(CardSuit.Spade, CardType.King)
        slot.placeRevealedCard(new_card)
        self.assertEqual(slot.card, new_card)
        self.assertFalse(slot.isFaceDown)

    def test_display_face_down_returns_placeholders(self):
        slot = CardSlot(0, 0)
        slot.placeHiddenCard(Card(CardSuit.Club, CardType.Three))
        self.assertEqual(slot.display(), "??")

    def test_display_face_up_returns_card_display(self):
        slot = CardSlot(0, 0)
        card = Card(CardSuit.Spade, CardType.Ten)
        slot.placeRevealedCard(card)
        self.assertEqual(slot.display(), card.display())

    def test_get_card_value_special_cases(self):
        slot = CardSlot(0, 0)
        # Ace -> 1
        slot.placeRevealedCard(Card(CardSuit.Heart, CardType.Ace))
        self.assertEqual(slot.get_card_value(), 1)
        # Two -> -2
        slot.placeRevealedCard(Card(CardSuit.Club, CardType.Two))
        self.assertEqual(slot.get_card_value(), -2)
        # Jack/Queen -> 10
        slot.placeRevealedCard(Card(CardSuit.Diamond, CardType.Jack))
        self.assertEqual(slot.get_card_value(), 10)
        slot.placeRevealedCard(Card(CardSuit.Spade, CardType.Queen))
        self.assertEqual(slot.get_card_value(), 10)
        # King -> 0
        slot.placeRevealedCard(Card(CardSuit.Heart, CardType.King))
        self.assertEqual(slot.get_card_value(), 0)

    def test_get_card_value_defaults_to_numeric_rank(self):
        slot = CardSlot(0, 0)
        for rank in [CardType.Three, CardType.Four, CardType.Five, CardType.Six,
                     CardType.Seven, CardType.Eight, CardType.Nine, CardType.Ten]:
            slot.placeRevealedCard(Card(CardSuit.Club, rank))
            self.assertEqual(slot.get_card_value(), rank.value)

    def test_get_card_value_raises_when_no_card(self):
        slot = CardSlot(0, 0)
        # Accessing self.card.type when card is None should raise AttributeError
        with self.assertRaises(AttributeError):
            _ = slot.get_card_value()


if __name__ == "__main__":
    unittest.main()
