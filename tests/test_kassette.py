import os
import unittest
from unittest import mock

from config import Config
from kassette import Kassette


class TestKassette(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None  # To see full diff in case of failure

    def test_example(self):
        kassette = Kassette("demo", config=Config())
        self.assertEqual(kassette.example, "demo")
        self.assertIsNotNone(kassette.config)

    def test_record(self):
        with mock.patch("subprocess.check_output") as mock_check_output:

            def fake_check_output(cmd, **kwargs):
                if "deploy" in cmd:
                    return b"""
 items:
 - kind: deploy
 """
                elif "service" in cmd:
                    return b"""
 items:
 - kind: service
 """

            mock_check_output.side_effect = fake_check_output

            kassette = Kassette("demo", config=Config(context="k8s-local"))
            with mock.patch("builtins.open") as mock_open:
                mock_open.return_value.__enter__.return_value.write = mock.Mock()

                kassette.record()
                mock_check_output.assert_has_calls(
                    [
                        mock.call(
                            [
                                "kubectl",
                                "get",
                                "deploy",
                                "-lapp.kubernetes.io/instance=demo,app.kubernetes.io/component=web",
                                "--output",
                                "yaml",
                                "--namespace",
                                "default",
                                "--context",
                                "k8s-local",
                            ]
                        ),
                        mock.call(
                            [
                                "kubectl",
                                "get",
                                "service",
                                "-lapp.kubernetes.io/instance=demo",
                                "--output",
                                "yaml",
                                "--namespace",
                                "default",
                                "--context",
                                "k8s-local",
                            ]
                        ),
                    ],
                    any_order=True,
                )

                mock_open.assert_has_calls(
                    [
                        mock.call("examples/demo/kassette.deploy.yaml", "w"),
                        mock.call().write("---\nitems:\n  - kind: deploy\n"),
                        mock.call("examples/demo/kassette.service.yaml", "w"),
                        mock.call().write("---\nitems:\n  - kind: service\n"),
                    ],
                    any_order=True,
                )

    def test_diff_success(self):
        with mock.patch("subprocess.check_output") as mock_check_output:

            def fake_check_output(cmd, **kwargs):
                if "deploy" in cmd:
                    return b"""
items:
- kind: deploy
"""
                elif "service" in cmd:
                    return b"""
items:
- kind: service
"""

            mock_check_output.side_effect = fake_check_output
            kassette = Kassette("demo", config=Config(context="k8s-local"))

            with mock.patch.object(
                kassette, "_Kassette__read_kassette"
            ) as mock_read_kassette:
                mock_read_kassette.side_effect = [
                    {"items": [{"kind": "deploy"}]},
                    {"items": [{"kind": "service"}]},
                ]
                res = kassette.diff(exit_on_error=False)
                self.assertEqual(res, (0, []))

    def test_diff_failure(self):
        with mock.patch("subprocess.check_output") as mock_check_output:

            def fake_check_output(cmd, **kwargs):
                if "deploy" in cmd:
                    return b"""
items:
- kind: deploy
  metadata:
    labels:
      something: new
"""
                elif "service" in cmd:
                    return b"""
items:
- kind: service
  metadata:
    labels:
      something: new
"""

            mock_check_output.side_effect = fake_check_output
            kassette = Kassette("demo", config=Config(context="k8s-local"))

            with mock.patch.object(
                kassette, "_Kassette__read_kassette"
            ) as mock_read_kassette:
                mock_read_kassette.side_effect = [
                    {
                        "items": [
                            {
                                "kind": "deploy",
                            }
                        ]
                    },
                    {"items": [{"kind": "service"}]},
                ]
                res = kassette.diff(exit_on_error=False)
                self.assertEqual(
                    (
                        1,
                        [
                            [
                                "--- \n",
                                "+++ \n",
                                "@@ -1,3 +1,6 @@\n",
                                " ---\n",
                                " items:\n",
                                "   - kind: deploy\n",
                                "+    metadata:\n",
                                "+      labels:\n",
                                "+        something: new\n",
                            ],
                            [
                                "--- \n",
                                "+++ \n",
                                "@@ -1,3 +1,5 @@\n",
                                " ---\n",
                                " items:\n",
                                "   - kind: service\n",
                                "+    metadata:\n",
                                "+      labels: {}\n",
                            ],
                        ],
                    ),
                    res,
                )

    def test_update(self):
        kassette = Kassette("demo", config=Config(context="k8s-local"))
        with mock.patch.object(
            kassette, "_Kassette__write_kassette"
        ) as mock_write_kassette:
            with mock.patch.object(
                kassette, "_Kassette__read_kassette"
            ) as mock_read_kassette:
                mock_read_kassette.return_value = {"items": [{"kind": "deploy"}]}
                kassette.update("deploy", ".items.[].update", "this")
                mock_write_kassette.assert_called_once_with(
                    "deploy",
                    {"items": [{"kind": "deploy", "update": "this"}]},
                )
