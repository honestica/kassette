from typing import Any

import yaml
from indent_dumper import IndentDumper


class Kyaml:
    @staticmethod
    def dump(data: dict[str, Any], stream: None = None, **kwargs: Any) -> Any:
        """
        Dump a Python object to a YAML formatted stream with indentation kubernetes style.
        """
        return yaml.dump(
            data, stream, Dumper=IndentDumper, explicit_start=True, **kwargs
        )

    @staticmethod
    def safe_load(stream: str, **kwargs: Any) -> Any:
        """
        Load a YAML formatted stream and return the corresponding Python object.
        """
        return yaml.safe_load(stream, **kwargs)
