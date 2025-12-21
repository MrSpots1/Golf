import unittest
import io
import sys
from unittest.mock import patch

import HumanPlayer
from PlayerType import PlayerType


class TestHumanPlayer(unittest.TestCase):
    def test_human_player_type(self):
        hp = HumanPlayer("Alice")
        self.assertEqual(hp.playerType, PlayerType.Human)

    def test_play_turn_prints_todo(self):
        hp = HumanPlayer("Bob")
        with io.StringIO() as buf, patch.object(sys, "stdout", buf):
            hp.playTurn(None)
            output = buf.getvalue()
        self.assertIn("TODO", output)
