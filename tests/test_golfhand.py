import unittest

from CardSlot import CardPosition
from GolfHand import GolfHand
from Card import Card
from CardSuit import CardSuit
from CardType import CardType


class TestGolfHand(unittest.TestCase):
    def test_init_grid_setup(self):
        hand = GolfHand()
        self.assertEqual(hand.rows, 2)
        self.assertEqual(hand.columns, 3)
        # All slots exist and start face down
        for r in range(hand.rows):
            for c in range(hand.columns):
                slot = hand.getSlot(CardPosition(r, c))
                self.assertTrue(slot.isFaceDown)
                self.assertIsNone(slot.card)

    def test_getSlot_bounds(self):
        hand = GolfHand()
        # Valid
        self.assertIsNotNone(hand.getSlot(CardPosition(0, 0)))
        self.assertIsNotNone(hand.getSlot(CardPosition(1, 2)))
        # Row out of bounds
        with self.assertRaises(IndexError):
            hand.getSlot(CardPosition(-1, 0))
        with self.assertRaises(IndexError):
            hand.getSlot(CardPosition(2, 0))
        # Column out of bounds
        with self.assertRaises(IndexError):
            hand.getSlot(CardPosition(0, -1))
        with self.assertRaises(IndexError):
            hand.getSlot(CardPosition(0, 3))

    def test_place_and_reveal_hidden_card(self):
        hand = GolfHand()
        card = Card(CardSuit.Heart, CardType.Ace)
        pos = CardPosition(0, 1)
        hand.placeFacedownCard(pos, card)
        slot = hand.getSlot(pos)
        self.assertTrue(slot.isFaceDown)
        self.assertIs(slot.card, card)
        hand.revealCard(pos)
        self.assertFalse(slot.isFaceDown)

    def test_place_revealed_card_sets_face_up(self):
        hand = GolfHand()
        card = Card(CardSuit.Spade, CardType.King)
        pos = CardPosition(1, 0)
        hand.placeRevealedCard(pos, card)
        slot = hand.getSlot(pos)
        self.assertFalse(slot.isFaceDown)
        self.assertIs(slot.card, card)

    def test_revealRemainingCards_and_is_done(self):
        hand = GolfHand()
        # Place hidden cards across the board
        for r in range(hand.rows):
            for c in range(hand.columns):
                hand.placeFacedownCard(CardPosition(r, c), Card(CardSuit.Club, CardType.Three))
        self.assertFalse(hand.is_done())
        hand.revealRemainingCards()
        self.assertTrue(hand.is_done())

    def test_calculate_value_pair_cancels_non_two(self):
        hand = GolfHand()
        # Column 0: pair of Fours revealed -> cancels to 0
        hand.placeRevealedCard(CardPosition(0, 0), Card(CardSuit.Diamond, CardType.Four))
        hand.placeRevealedCard(CardPosition(1, 0), Card(CardSuit.Heart, CardType.Four))
        # Column 1: one revealed Seven -> counts 7
        hand.placeRevealedCard(CardPosition(0, 1), Card(CardSuit.Spade, CardType.Seven))
        # Column 2: both revealed Ace + King -> 1 + 0 = 1
        hand.placeRevealedCard(CardPosition(0, 2), Card(CardSuit.Club, CardType.Ace))
        hand.placeRevealedCard(CardPosition(1, 2), Card(CardSuit.Spade, CardType.King))
        score = hand.calculate_current_hand_value()
        self.assertEqual(score, 0 + 7 + 1)

    def test_calculate_value_twos_do_not_cancel(self):
        hand = GolfHand()
        # Column 0: pair of Twos revealed -> sums -2 + -2 = -4
        hand.placeRevealedCard(CardPosition(0, 0), Card(CardSuit.Club, CardType.Two))
        hand.placeRevealedCard(CardPosition(1, 0), Card(CardSuit.Heart, CardType.Two))
        # Column 1: only bottom revealed Nine -> counts 9
        hand.placeFacedownCard(CardPosition(0, 1), Card(CardSuit.Spade, CardType.Five))
        hand.placeRevealedCard(CardPosition(1, 1), Card(CardSuit.Diamond, CardType.Nine))
        # Column 2: both face down -> ignored
        score = hand.calculate_current_hand_value()
        self.assertEqual(score, -4 + 9)

    def test_clone_preserves_state_and_cards(self):
        hand = GolfHand()
        # Mixed states: hidden and revealed
        a = Card(CardSuit.Heart, CardType.Ace)
        k = Card(CardSuit.Spade, CardType.King)
        t = Card(CardSuit.Club, CardType.Two)
        hand.placeFacedownCard(CardPosition(0, 0), a)
        hand.placeRevealedCard(CardPosition(0, 1), k)
        hand.placeFacedownCard(CardPosition(1, 2), t)
        # Reveal one
        hand.revealCard(CardPosition(0, 0))
        clone = hand.clone()
        for r in range(hand.rows):
            for c in range(hand.columns):
                orig = hand.getSlot(CardPosition(r, c))
                cp = clone.getSlot(CardPosition(r, c))
                self.assertEqual(orig.isFaceDown, cp.isFaceDown)
                self.assertIs(orig.card, cp.card)


if __name__ == "__main__":
    unittest.main()
