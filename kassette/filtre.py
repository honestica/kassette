import re
from typing import Any


class Filter:
    @staticmethod
    def filter_in(tree: Any, filtres: list[str], path: str = "") -> Any:
        if filtres == []:
            return tree

        n_tree: None | dict[Any, Any] | list[Any] = None
        if isinstance(tree, dict):
            n_tree = {}
            for key, val in tree.items():
                n_path = Filter.build_path(path, key)
                if n_path in filtres:
                    n_tree[key] = val
                else:
                    for filtre in filtres:
                        if re.search(r"^{}\.".format(re.escape(n_path)), filtre):
                            n_tree[key] = Filter.filter_in(val, filtres, n_path)
        elif isinstance(tree, list):
            n_path = Filter.build_path(path, [])
            n_tree = []
            if n_path in filtres:
                n_tree = tree
            else:
                for element in tree:
                    should_be_kept = False
                    for filtre in filtres:
                        if re.search(r"^{}\.".format(re.escape(n_path)), filtre):
                            should_be_kept = True
                            element = Filter.filter_in(element, filtres, n_path)
                    if should_be_kept:
                        n_tree.append(element)
        return n_tree

    @staticmethod
    def filter_out(tree: Any, filtres: list[str], path: str = "") -> Any:
        if filtres == []:
            return tree

        if isinstance(tree, dict):
            n_d_tree = {}
            for key, val in tree.items():
                n_path = Filter.build_path(path, key)
                if n_path not in filtres:
                    n_d_tree[key] = Filter.filter_out(val, filtres, n_path)
            return n_d_tree
        elif isinstance(tree, list):
            n_l_tree = []
            n_path = Filter.build_path(path, [])
            if n_path not in filtres:
                for element in tree:
                    if n_path not in filtres:
                        n_l_tree.append(Filter.filter_out(element, filtres, n_path))
            return n_l_tree
        return tree

    @staticmethod
    def build_path(parent: str, child: str | list[str]) -> str:
        if isinstance(child, list):
            return "{}.[]".format(parent)
        else:
            if re.search(r"\.", child):
                return "{}.{}".format(parent, "{" + child + "}")
        return "{}.{}".format(parent, child)
