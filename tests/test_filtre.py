import unittest

from filtre import Filter


class TestFilter(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None  # Disable diff output for better readability

    def test_build_path(self):
        filter_instance = Filter()
        self.assertEqual(
            filter_instance.build_path("", "items"),
            ".items",
        )
        self.assertEqual(
            filter_instance.build_path(".items", ["a", "b"]),
            ".items.[]",
        )
        self.assertEqual(
            filter_instance.build_path(".items", "a"),
            ".items.a",
        )
        self.assertEqual(
            filter_instance.build_path("", []),
            ".[]",
        )
        self.assertEqual(
            filter_instance.build_path("", "helm.sh/chart"), ".{helm.sh/chart}"
        )
        self.assertEqual(
            filter_instance.build_path(".items.[].metadata.labels", "helm.sh/chart"),
            ".items.[].metadata.labels.{helm.sh/chart}",
        )

    def test_filter_in(self):
        filter_instance = Filter()
        tree = {
            "items": [
                {
                    "metadata": {
                        "name": "item1",
                        "labels": {"helm.sh/chart": "chart1", "some": "other"},
                    }
                },
            ]
        }
        filtres = [".items.[].metadata.labels.{helm.sh/chart}"]
        expected = {
            "items": [
                {"metadata": {"labels": {"helm.sh/chart": "chart1"}}},
            ]
        }
        result = filter_instance.filter_in(tree, filtres)
        self.assertEqual(result, expected)

    def test_filter_out(self):
        filter_instance = Filter()
        tree = {
            "items": [
                {
                    "metadata": {
                        "name": "item1",
                        "labels": {"helm.sh/chart": "chart1", "some": "other"},
                    }
                },
            ]
        }
        filtres = [".items.[].metadata.labels.{helm.sh/chart}"]
        expected = {
            "items": [
                {"metadata": {"name": "item1", "labels": {"some": "other"}}},
            ]
        }
