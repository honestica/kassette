import yaml


class IndentDumper(yaml.Dumper):

    def increase_indent(self, flow: bool = False, indentless: bool = False) -> None:
        return super(IndentDumper, self).increase_indent(flow, False)
