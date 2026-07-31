import subprocess
from typing import Any

import yaml


class Kube:
    def __init__(self, namespace: str = "default", context: str | None = None) -> None:
        self.namespace = namespace
        self.context = context

    def get(self, kind: str, **kwargs: Any) -> Any:
        labels = []
        for label, value in kwargs.get("labels", {}).items():
            labels.append(f"{label}={value}")

        return self.__kubectl_get([kind, "-l" + ",".join(labels)])

    def __kubectl_get(self, cmd: list[str]) -> Any:
        command = (
            ["kubectl", "get"]
            + cmd
            + ["--output", "yaml"]
            + ["--namespace", self.namespace]
        )
        if self.context:
            command = command + ["--context", self.context]
        result = subprocess.check_output(command)
        return yaml.safe_load(result)
