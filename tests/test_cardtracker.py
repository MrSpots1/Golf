import unittest
from CardTracker import CardTracker
from CardType import CardType
from CardSuit import CardSuit
from Card import Card


class TestCardTracker(unittest.TestCase):
    def test_initial_counts(self):
        ct = CardTracker(numberOfDecks=1)
        self.assertEqual(0, ct.getTotalObservedCards())
        # For one deck, each type has 4 remaining initially
        for t in CardType:
            self.assertEqual(ct.getRemainingCount(t), 4)
            # initial probability should be 4/52 for any specific type
            self.assertEqual(ct.getProbabilityOfDrawing(t), 4/52)
        self.assertEqual(ct.getTotalRemainingCards(), 52)
    
    def test_initial_multi_deck_counts(self):
        ct = CardTracker(numberOfDecks=2)
        self.assertEqual(0, ct.getTotalObservedCards())
        # For two decks, each type has 8 remaining initially
        for t in CardType:
            self.assertEqual(ct.getRemainingCount(t), 8)
            # initial probability should be 8/104 for any specific type
            self.assertEqual(ct.getProbabilityOfDrawing(t), 8/104)
        self.assertEqual(ct.getTotalRemainingCards(), 104)

    def test_observe_card_updates_counts(self):
        ct = CardTracker(numberOfDecks=1)
        ace_spade = Card(CardSuit.Spade, CardType.Ace)
        ct.observeCard(ace_spade)
        # Ace remaining decreases by 1
        self.assertEqual(ct.getRemainingCount(CardType.Ace), 3)
        # Total remaining decreases by 1
        self.assertEqual(ct.getTotalRemainingCards(), 51)

    def test_probability(self):
        ct = CardTracker(numberOfDecks=1)
        # Initially: 4/52 for any specific type
        self.assertAlmostEqual(ct.getProbabilityOfDrawing(CardType.King), 4/52)
        # After observing a King, remaining is 3/51
        ct.observeCard(Card(CardSuit.Heart, CardType.King))
        self.assertAlmostEqual(ct.getProbabilityOfDrawing(CardType.King), 3/51)

    def test_probability_when_no_cards_left(self):
        ct = CardTracker(numberOfDecks=1)
        # Observe all cards (simulate deck exhaustion)
        for suit in CardSuit:
            for card_type in CardType:
                ct.observeCard(Card(suit, card_type))
        self.assertEqual(ct.getTotalRemainingCards(), 0)
        self.assertEqual(ct.getProbabilityOfDrawing(CardType.Two), 0.0)
