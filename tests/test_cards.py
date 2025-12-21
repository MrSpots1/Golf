import unittest
from CardSuit import CardSuit
from CardType import CardType


class TestCardEnums(unittest.TestCase):
    def test_cardsuit_members(self):
        self.assertEqual(CardSuit.Heart.value, 1)
        self.assertEqual(CardSuit.Diamond.value, 2)
        self.assertEqual(CardSuit.Club.value, 3)
        self.assertEqual(CardSuit.Spade.value, 4)

    def test_cardtype_members(self):
        self.assertEqual(CardType.Ace.value, 1)
        self.assertEqual(CardType.Two.value, 2)
        self.assertEqual(CardType.Three.value, 3)
        self.assertEqual(CardType.Four.value, 4)
        self.assertEqual(CardType.Five.value, 5)
        self.assertEqual(CardType.Six.value, 6)
        self.assertEqual(CardType.Seven.value, 7)
        self.assertEqual(CardType.Eight.value, 8)
        self.assertEqual(CardType.Nine.value, 9)
        self.assertEqual(CardType.Ten.value, 10)
        self.assertEqual(CardType.Jack.value, 11)
        self.assertEqual(CardType.Queen.value, 12)
        self.assertEqual(CardType.King.value, 13)
