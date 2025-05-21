import unittest
from unittest import mock

from kube import Kube


class TestKube(unittest.TestCase):
    def test_get(self):
        with mock.patch("kube.subprocess.check_output") as mock_check_output:
            mock_check_output.return_value = b"""
items:
  - kind: Pod
    metadata:
        name: test-pod
        labels:
            app: test
    spec:
        containers:
        - name: test-container
"""
            kube = Kube(context="test-context", namespace="test-namespace")
            result = kube.get("pods", labels={"app": "test"})
            mock_check_output.assert_called_once_with(
                [
                    "kubectl",
                    "get",
                    "pods",
                    "-lapp=test",
                    "--output",
                    "yaml",
                    "--namespace",
                    "test-namespace",
                    "--context",
                    "test-context",
                ]
            )
            self.assertIn("items", result)
            self.assertEqual(len(result["items"]), 1)
            self.assertEqual(result["items"][0]["kind"], "Pod")
            self.assertEqual(result["items"][0]["metadata"]["name"], "test-pod")
