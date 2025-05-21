from typing import Any


class Hash:
    @staticmethod
    def deep_merge(dct: Any, merge_dct: Any, cumulative_list: bool = False) -> None:
        for k in merge_dct:
            if k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], dict):
                Hash.deep_merge(dct[k], merge_dct[k], cumulative_list)
            elif (
                k in dct and isinstance(dct[k], list) and isinstance(merge_dct[k], list)
            ):
                if cumulative_list:
                    dct[k].extend(merge_dct[k])
                else:
                    dct[k] = merge_dct[k]
            else:
                dct[k] = merge_dct[k]
