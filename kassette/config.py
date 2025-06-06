import logging
import sys
from typing import Any

import yaml
from hash import Hash


class Config:
    def __init__(
        self,
        config_file: str = "kassette.yaml",
        namespace: str = "default",
        context: str | None = None,
    ):
        self.namespace = namespace
        self.context = context
        self._config_file = config_file
        self._config = {}
        self._examples_configs: dict[str, "ExampleConfig"] = {}

        try:
            with open(self._config_file, "r") as config_f:
                self._config = yaml.safe_load(config_f.read())["config"]
        except FileNotFoundError:
            logging.warning(f"Configuration file '{self._config_file}' not found.")
        except yaml.YAMLError as exc:
            logging.error(f"Error parsing YAML file: {exc}")
            sys.exit(1)

    @property
    def main(self) -> dict[str, Any]:
        """
        Return the main configuration.
        """
        return self._config

    @property
    def examples_dir(self) -> str:
        """
        Return the directory containing the examples.
        """
        this_dir = self.main.get("examples_dir", "examples")
        if not isinstance(this_dir, str):
            logging.warning(
                'Configuration "examples_dir" is not set to a string, using default "examples".'
            )
            return "examples"
        return this_dir

    def example(self, it: str) -> "ExampleConfig":
        """
        Load the configuration for a specific example.
        """
        if it in self._examples_configs:
            return self._examples_configs[it]

        base_config = self.main.copy()
        try:
            with open(f"{self.examples_dir}/{it}/kassette.yaml", "r") as config_f:
                Hash().deep_merge(
                    base_config, yaml.safe_load(config_f.read())["config"], True
                )

        except FileNotFoundError:
            logging.warning(
                f'No kassette configuration (kassette.yaml) found for "{it}" in #{self.examples_dir}, create it 😉'
            )
        except yaml.YAMLError as exc:
            logging.error(f"Error parsing YAML file: {exc}")
            sys.exit(1)

        self._examples_configs[it] = ExampleConfig(it, base_config, self)
        return self._examples_configs[it]


class ExampleConfig:
    def __init__(self, name: str, config: dict[str, Any], parent: Config):
        self.name = name
        self.config = config
        self._parent = parent

    @property
    def context(self) -> str | None:
        """
        Return the context for a specific example.
        """
        return self._parent.context

    @property
    def namespace(self) -> str:
        """
        Return the namespace for a specific example.
        """
        return self._parent.namespace

    @property
    def dir(self) -> str:
        """
        Return the directory for a specific example.
        """
        return f"{self._parent.examples_dir}/{self.name}"

    def filters(self, kind: str, direction: str) -> list[str]:
        """
        Return the filters for a specific example.
        """
        if "kinds" not in self.config:
            return []
        if kind not in self.config["kinds"]:
            return []
        if "filters" not in self.config["kinds"][kind]:
            return []
        if direction not in self.config["kinds"][kind]["filters"]:
            return []

        paths = self.config["kinds"][kind]["filters"][direction]
        if not isinstance(paths, list):
            logging.warning(
                f'Example "{self.name}" has "filters" for kind "{kind}" and direction "{direction}" set to a non-list value.'
            )
            return []

        return paths

    def kinds(self) -> dict[str, Any]:
        """
        Return the kinds defined for this example.
        """
        if "kinds" not in self.config:
            return {}

        kinds = self.config["kinds"]
        if not isinstance(kinds, dict):
            logging.warning(
                f'Example "{self.name}" has "kinds" set to a non-dictionary value.'
            )
            return {}

        return kinds

    def has_kind(self, kind: str) -> bool:
        """
        Check if the example has a specific kind.
        """
        if "kinds" not in self.config:
            return False

        if kind not in self.config["kinds"]:
            return False

        if "enabled" not in self.config["kinds"][kind]:
            return False

        enabled = self.config["kinds"][kind]["enabled"]
        if not isinstance(enabled, bool):
            logging.warning(
                f'Kind "{kind}" in example "{self.name}" has "enabled" set to a non-boolean value.'
            )
            return False
        return enabled

    def labels_for_kind(self, kind: str) -> dict[str, str]:
        """
        Return the labels for a specific example and kind.
        """
        labels = {}

        if "labels" in self.config:
            labels = self.config["labels"].copy()

        if "kinds" not in self.config:
            return labels

        if kind not in self.config["kinds"]:
            return labels

        if "labels" not in self.config["kinds"][kind]:
            return labels

        Hash().deep_merge(labels, self.config["kinds"][kind]["labels"])
        return labels
