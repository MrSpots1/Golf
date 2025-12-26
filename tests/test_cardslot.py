import unittest

from CardSlot import CardPosition, CardSlot
from Card import Card
from CardSuit import CardSuit
from CardType import CardType


class TestCardSlot(unittest.TestCase):
    def test_initial_state(self):
        slot = CardSlot(CardPosition(0, 1))
        self.assertIsNone(slot.card)
        self.assertTrue(slot.isFaceDown)
        self.assertEqual(slot.position.row, 0)
        self.assertEqual(slot.position.column, 1)

    def test_place_hidden_card_sets_card_and_face_down(self):
        slot = CardSlot(CardPosition(0, 0))
        card = Card(CardSuit.Heart, CardType.Five)
        slot.placeFacedownCard(card)
        self.assertEqual(slot.card, card)
        self.assertTrue(slot.isFaceDown)
        # str should be hidden
        self.assertEqual(slot.str(), "??")

    def test_place_hidden_card_raises_if_already_has_card(self):
        slot = CardSlot(CardPosition(0,0))
        first = Card(CardSuit.Club, CardType.Two)
        slot.placeFacedownCard(first)
        with self.assertRaises(ValueError):
            slot.placeFacedownCard(Card(CardSuit.Spade, CardType.Ace))

    def test_reveal_card_changes_state_and_raises_if_already_revealed(self):
        slot = CardSlot(CardPosition(0,0))
        # reveal with no card present still flips face state per implementation
        slot.revealCard()
        self.assertFalse(slot.isFaceDown)
        # second reveal should raise
        with self.assertRaises(ValueError):
            slot.revealCard()

    def test_place_revealed_card_sets_card_and_face_up(self):
        slot = CardSlot(CardPosition(0,0))
        card = Card(CardSuit.Diamond, CardType.Queen)
        slot.placeRevealedCard(card)
        self.assertEqual(slot.card, card)
        self.assertFalse(slot.isFaceDown)
        # str should show the card string
        self.assertEqual(slot.str(), card.str())

    def test_place_revealed_overwrites_existing_card(self):
        slot = CardSlot(CardPosition(0,0))
        slot.placeFacedownCard(Card(CardSuit.Heart, CardType.Nine))
        new_card = Card(CardSuit.Spade, CardType.King)
        slot.placeRevealedCard(new_card)
        self.assertEqual(slot.card, new_card)
        self.assertFalse(slot.isFaceDown)

    def test_str_face_down_returns_placeholders(self):
        slot = CardSlot(CardPosition(0,0))
        slot.placeFacedownCard(Card(CardSuit.Club, CardType.Three))
        self.assertEqual(slot.str(), "??")

    def test_str_face_up_returns_card_str(self):
        slot = CardSlot(CardPosition(0,0))
        card = Card(CardSuit.Spade, CardType.Ten)
        slot.placeRevealedCard(card)
        self.assertEqual(slot.str(), card.str())

    def test_get_card_value_special_cases(self):
        slot = CardSlot(CardPosition(0,0))
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
        slot = CardSlot(CardPosition(0,0))
        for rank in [CardType.Three, CardType.Four, CardType.Five, CardType.Six,
                     CardType.Seven, CardType.Eight, CardType.Nine, CardType.Ten]:
            slot.placeRevealedCard(Card(CardSuit.Club, rank))
            self.assertEqual(slot.get_card_value(), rank.value)

    def test_get_card_value_raises_when_no_card(self):
        slot = CardSlot(CardPosition(0,0))
        # Accessing self.card.type when card is None should raise AttributeError
        with self.assertRaises(AttributeError):
            _ = slot.get_card_value()


if __name__ == "__main__":
    unittest.main()
