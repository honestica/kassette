import unittest

from hash import Hash


class TestHash(unittest.TestCase):
    def test_deep_merge(self):
        dct1 = {"a": 1, "b": {"c": 2}}
        dct2 = {"b": {"d": 3}, "e": 4}
        expected = {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}

        Hash.deep_merge(dct1, dct2)
        self.assertEqual(dct1, expected)

    def test_deep_merge_nested(self):
        dct3 = {"x": {"y": {"z": 5}}}
        dct4 = {"x": {"y": {"w": 6}}}
        expected_nested = {"x": {"y": {"z": 5, "w": 6}}}

        Hash.deep_merge(dct3, dct4)
        self.assertEqual(dct3, expected_nested)

    def test_deep_merge_cumulative_list(self):
        dct5 = {"items": [1, 2]}
        dct6 = {"items": [3, 4]}
        Hash.deep_merge(dct5, dct6, True)
        self.assertEqual(dct5, {"items": [1, 2, 3, 4]})

        dct7 = {"other": "data"}
        dct8 = {"items": [3, 4]}
        Hash.deep_merge(dct7, dct8, True)
        self.assertEqual(dct7, {"other": "data", "items": [3, 4]})

        dct9 = {"items": [1, 2]}
        dct10 = {"other": "data"}
        Hash.deep_merge(dct9, dct10, True)
        self.assertEqual(dct9, {"items": [1, 2], "other": "data"})

        dct11 = {"items": "weird"}
        dct12 = {"items": [3, 4]}
        Hash.deep_merge(dct11, dct12, True)
        self.assertEqual(dct11, {"items": [3, 4]})

        dct13 = {"items": [3, 4]}
        dct14 = {"items": "weird"}
        Hash.deep_merge(dct13, dct14, True)
        self.assertEqual(dct13, {"items": "weird"})

        dct15 = {"items": {"filters": [1, 2]}}
        dct16 = {"items": {"filters": [3, 4]}}
        Hash.deep_merge(dct15, dct16, True)
        self.assertEqual(dct15, {"items": {"filters": [1, 2, 3, 4]}})
