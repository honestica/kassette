import difflib
import logging
import os
import re
import sys
from typing import Any

from config import Config
from filtre import Filter
from kube import Kube
from kyaml import Kyaml


class Kassette:
    def __init__(self, example: str, config: Config):
        self.example = example
        self.config = config.example(example)
        self.kube = Kube(self.config.namespace, self.config.context)

    def record(self) -> None:
        for kind, details in self.config.kinds().items():
            logging.info(
                "Recording kassette for example {} kind {} 📼".format(
                    self.example, kind
                )
            )
            if not details["enabled"]:
                self.__remove_kassette(kind)
                continue

            record = self.kube.get(kind, labels=self.config.labels_for_kind(kind))
            record = Filter.filter_in(
                record,
                self.config.filters(kind, "in"),
            )
            record = Filter.filter_out(
                record,
                self.config.filters(kind, "out"),
            )

            self.__write_kassette(kind, record)

    def diff(self, exit_on_error: bool = True) -> tuple[int, list[list[str]]]:
        exit_code = 0
        diffs = []
        for kind, details in self.config.kinds().items():
            if "enabled" in details:
                if not details["enabled"]:
                    continue
            kassette = self.__read_kassette(kind)
            if not kassette:
                raise FileNotFoundError(
                    'Error reading kassette in "{}" for kind "{}"'.format(
                        self.example, kind
                    )
                )

            new_record = self.kube.get(kind, labels=self.config.labels_for_kind(kind))
            new_record = Filter.filter_in(
                new_record,
                self.config.filters(kind, "in"),
            )
            new_record = Filter.filter_out(
                new_record,
                self.config.filters(kind, "out"),
            )

            s = difflib.SequenceMatcher(
                None,
                Kyaml.dump(kassette).splitlines(keepends=True),
                Kyaml.dump(new_record).splitlines(keepends=True),
            )
            expected_minimal_ratio = 1.0
            if "expected_percent_similarity" in details:
                expected_minimal_ratio = details["expected_percent_similarity"] / 100.0
            if s.ratio() < expected_minimal_ratio:
                logging.error(
                    'Difference ({}%) in "{}" for kind "{}":'.format(
                        round(100.0 - s.ratio() * 100.0, 2),
                        self.example,
                        kind,
                    )
                )
                diff = difflib.unified_diff(
                    Kyaml.dump(kassette).splitlines(keepends=True),
                    Kyaml.dump(new_record).splitlines(keepends=True),
                )
                diff_lines = list(diff)
                diffs.append(diff_lines)
                sys.stdout.writelines(diff_lines)
                exit_code = 1
        if exit_code == 0:
            logging.info("Kassette replay is correct 📼")
        if exit_on_error and exit_code != 0:
            logging.error("Kassette replay is incorrect 😱")
        return (exit_code, diffs)

    def update(self, kind: str, path: str, value: str) -> None:
        data = self.__read_kassette(kind)
        self.__update(path, value, data)
        self.__write_kassette(kind, data)

    def __update(self, path: str, value: str, tree: Any) -> None:
        array_matcher = re.search(r"^\.\[\](?P<sub_path>.*)$", path)
        end_path_matcher_dot = re.search(r"^\.{(?P<last_elt>[^}]+)}$", path)
        end_path_matcher = re.search(r"^\.(?P<last_elt>[^\.]+)$", path)

        if array_matcher:
            sub_path = array_matcher.group("sub_path")
            for sub_tree in tree:
                self.__update(sub_path, value, sub_tree)
        elif end_path_matcher_dot:
            elt = end_path_matcher_dot.group("last_elt")
            tree[elt] = value
        elif end_path_matcher:
            elt = end_path_matcher.group("last_elt")
            tree[elt] = value
        else:
            matcher = re.search(r"^\.(?P<elt>{[^}]+}|[^\.]+)(?P<sub_path>.*)", path)
            if not matcher:
                logging.error(
                    'Invalid path "{}" for updating kassette "{}"'.format(
                        path, self.example
                    )
                )
                return
            elt = matcher.group("elt")
            sub_path = matcher.group("sub_path")
            self.__update(sub_path, value, tree[elt])

    def __remove_kassette(self, kind: str) -> None:
        kassette_path = self.config.dir + "/kassette." + kind + ".yaml"
        if os.path.exists(kassette_path):
            os.remove(kassette_path)

    def __write_kassette(self, kind: str, data: Any) -> None:
        f = open(self.config.dir + "/kassette." + kind + ".yaml", "w")
        f.write(Kyaml.dump(data))
        f.close()

    def __read_kassette(self, kind: str) -> Any:
        f = open(self.config.dir + "/kassette." + kind + ".yaml")
        data = Kyaml.safe_load(f.read())
        f.close()

        return data
