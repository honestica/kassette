import unittest

import yaml
from indent_dumper import IndentDumper


class TestIndentDumper(unittest.TestCase):
    def test_indentation(self):
        self.assertEqual(
            yaml.dump({"array": ["a", "b"]}, Dumper=IndentDumper),
            "array:\n  - a\n  - b\n",
        )
