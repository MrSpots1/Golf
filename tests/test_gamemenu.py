import unittest
from unittest.mock import patch
import io
import sys

from GameMenu import GameMenu


class TestGameMenu(unittest.TestCase):
    def test_display_outputs_menu(self):
        gm = GameMenu()
        with io.StringIO() as buf, patch.object(sys, "stdout", buf):
            gm.display()
            output = buf.getvalue()
        # Ensure key menu lines appear
        self.assertIn("=== Golf: Main Menu ===", output)
        self.assertIn("1) Start new game vs AI", output)
        self.assertIn("2) Start new game vs Player", output)
        self.assertIn("3) Display rules", output)
        self.assertIn("q) Quit", output)

    def test_run_quit(self):
        gm = GameMenu()
        with patch("builtins.input", side_effect=["q"]), io.StringIO() as buf, patch.object(sys, "stdout", buf):
            gm.run()
            output = buf.getvalue()
        self.assertIn("Goodbye!", output)

    def test_run_ai_start(self):
        gm = GameMenu()
        with patch("builtins.input", side_effect=["1", "q"]), io.StringIO() as buf, patch.object(sys, "stdout", buf):
            gm.run()
            output = buf.getvalue()
        self.assertIn("Starting a new game against AI", output)

    def test_run_player_start(self):
        gm = GameMenu()
        with patch("builtins.input", side_effect=["2", "q"]), io.StringIO() as buf, patch.object(sys, "stdout", buf):
            gm.run()
            output = buf.getvalue()
        self.assertIn("Starting a new game against another player", output)

    def test_run_show_rules(self):
        gm = GameMenu()
        with patch("builtins.input", side_effect=["3", "q"]), io.StringIO() as buf, patch.object(sys, "stdout", buf):
            gm.run()
            output = buf.getvalue()
        self.assertIn("Golf Rules", output)
