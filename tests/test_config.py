import unittest

from config import Config


class TestConfig(unittest.TestCase):
    def test_main(self):
        config = Config()
        self.assertIn("examples_dir", config.main)
        self.assertEqual(config.main["examples_dir"], "examples")

    def test_examples_dir(self):
        config = Config()
        self.assertEqual(config.examples_dir, "examples")

    def test_namespace(self):
        config = Config()
        self.assertEqual(config.namespace, "default")

    def test_context(self):
        config = Config(context="test-context")
        self.assertEqual(config.context, "test-context")


class TestExampleConfig(unittest.TestCase):
    def test_dir(self):
        config = Config().example("demo")
        self.assertEqual(config.dir, "examples/demo")

    def test_main_filters(self):
        config = Config().example("demo")

        filters_in = config.filters("pod", "in")
        self.assertIsInstance(filters_in, list)
        self.assertEqual(len(filters_in), 0)

        filters_out = config.filters("pod", "out")
        self.assertIsInstance(filters_out, list)
        self.assertEqual(len(filters_out), 0)

        deploy_filters_in = config.filters("deploy", "in")
        self.assertIsInstance(deploy_filters_in, list)
        self.assertEqual(len(deploy_filters_in), 0)

        deploy_filters_out = config.filters("deploy", "out")
        self.assertIsInstance(deploy_filters_out, list)
        self.assertGreater(len(deploy_filters_out), 0)
        self.assertIn(".items.[].status", deploy_filters_out)
        self.assertNotIn(".items.[].metadata.labels.notthere", deploy_filters_out)

        svc_filters_out = config.filters("service", "out")
        self.assertIsInstance(svc_filters_out, list)
        self.assertGreater(len(svc_filters_out), 0)
        self.assertIn(".items.[].metadata.uid", svc_filters_out)
        self.assertIn(".items.[].metadata.labels.something", svc_filters_out)
        self.assertNotIn(".items.[].metadata.labels.notthere", svc_filters_out)

    def test_kinds(self):
        config = Config().example("demo")
        kinds = config.kinds()

        self.assertIsInstance(kinds, dict)
        self.assertGreater(len(kinds), 0)
        self.assertIn("deploy", kinds)

    def test_example_has_kind(self):
        config = Config().example("demo")
        self.assertTrue(config.has_kind("deploy"))
        self.assertTrue(config.has_kind("service"))
        self.assertFalse(config.has_kind("secret"))
        self.assertFalse(config.has_kind("configmap"))

    def test_example_labels_for_kind(self):
        config = Config().example("demo")
        labels = config.labels_for_kind("deploy")

        self.assertIsInstance(labels, dict)
        self.assertEqual(
            labels,
            {
                "app.kubernetes.io/instance": "demo",
                "app.kubernetes.io/component": "web",
            },
        )

        svc_labels = config.labels_for_kind("service")
        self.assertIsInstance(svc_labels, dict)
        self.assertEqual(
            svc_labels,
            {
                "app.kubernetes.io/instance": "demo",
            },
        )
