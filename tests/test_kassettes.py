import unittest

from config import Config
from kassettes import Kassettes


class TestKassettes(unittest.TestCase):
    def test_all(self):
        kassettes = Kassettes(Config())
        all_kassettes = kassettes.all()
        self.assertIsInstance(all_kassettes, list)
        self.assertGreater(len(all_kassettes), 0)
        self.assertEqual(all_kassettes[0].example, "demo")

    def test_filter_kind(self):
        kassettes = Kassettes(Config())
        filtered_kassettes = kassettes.filter_kind("deploy")
        self.assertIsInstance(filtered_kassettes, list)
        self.assertEqual(len(filtered_kassettes), 1)
