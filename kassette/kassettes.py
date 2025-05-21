import glob
import logging
import os

from config import Config

from kassette import Kassette


class Kassettes:
    def __init__(self, config: Config):
        self.config = config

    def all(self) -> list[Kassette]:
        _all = []
        for example_dir in glob.glob(f"{self.config.examples_dir}/*"):
            example = os.path.basename(example_dir)
            if not os.path.isfile(f"{example_dir}/kassette.yaml"):
                logging.warning(
                    f"No kassette configuration (kassette.yaml) found for {example}, skipping..."
                )
                continue
            _all.append(
                Kassette(
                    example,
                    config=self.config,
                )
            )
        return _all

    def filter_kind(self, kind: str) -> list[Kassette]:
        return list(filter(lambda k: k.config.has_kind(kind), self.all()))
