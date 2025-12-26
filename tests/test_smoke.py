import importlib
import unittest


class TestImports(unittest.TestCase):
    def test_imports(self):
        modules = [
            "CardSuit",
            "CardType",
            "Card",
        ]
        for name in modules:
            importlib.import_module(name)
