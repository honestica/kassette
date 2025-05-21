import unittest

from kyaml import Kyaml


class TestKyaml(unittest.TestCase):
    def test_dump(self):
        self.assertEqual(
            Kyaml.dump({"array": ["a", "b"]}),
            "---\narray:\n  - a\n  - b\n",
        )

    def test_safe_load(self):
        self.assertEqual(
            Kyaml.safe_load("array:\n  - a\n  - b\n"),
            {"array": ["a", "b"]},
        )
