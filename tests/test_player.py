import unittest
import io
import sys
from unittest.mock import patch

from HumanPlayer import HumanPlayer
from PlayerType import PlayerType


class TestHumanPlayer(unittest.TestCase):
    def test_human_player_type(self):
        hp = HumanPlayer("Alice", 0)
        self.assertEqual(hp.playerType, PlayerType.Human)
