import unittest
from unittest import mock

from kassette import run


class TestRun(unittest.TestCase):
    def test_diff_without_difference_exits_with_zero(self):
        with mock.patch("sys.argv", ["kassette", "diff", "demo"]):
            with mock.patch("kassette.Kassette") as mock_kassette:
                mock_kassette.return_value.diff.return_value = (0, [])
                with self.assertRaises(SystemExit) as cm:
                    run()
        self.assertEqual(cm.exception.code, 0)

    def test_diff_with_difference_exits_with_one(self):
        with mock.patch("sys.argv", ["kassette", "diff", "demo"]):
            with mock.patch("kassette.Kassette") as mock_kassette:
                mock_kassette.return_value.diff.return_value = (1, [["-a\n", "+b\n"]])
                with self.assertRaises(SystemExit) as cm:
                    run()
        self.assertEqual(cm.exception.code, 1)
