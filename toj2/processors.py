import pathlib
import json
from jinja2 import Environment, FileSystemLoader
from .context import AppContext
from .jinja2_custom_filter import stable_groupby, datef, csvcell
from .excel.excel_custom_filter import excel_time
from .utils import get_stream
class Processor:
    def __init__(self, context:AppContext) -> None:
        self.context = context
        self._setup()

    def _setup (self):
        pass

    def execute(self, load_result:dict) -> None:
        load_result['params'] = self.context.parameters
        self._execute(load_result)

    def out_stream(self):
        return get_stream(source = self.context.out ,mode = 'w', 
                            encoding = self.context.output_encoding,
                        )

    def _execute(self, load_result) -> None:
            pass


class Jinja2Processor(Processor):
    def __init__(self, context:AppContext) -> None:
        super().__init__(context)
    
    def _setup(self) -> None:
        """jinja2テンプレート生成"""
        path = pathlib.Path(self.context.template)
        environment = Environment(loader=FileSystemLoader(
            path.parent, encoding=self.context.template_encoding))
        self._install_filters(environment=environment)
        self.template = environment.get_template(path.name)

    def _install_filters(self, environment: Environment) -> None:
        """追加のフィルタを設定する"""
        environment.filters['stable_groupby'] = stable_groupby
        environment.filters['datef'] = datef
        environment.filters['excel_time'] = excel_time
        environment.filters['csvcell'] = csvcell

    def _execute(self, load_result:dict) -> None:
        with self.out_stream() as dest:
            dest.write(self.template.render(load_result))

class DumpProcessor(Processor):
    def __init__(self, context:AppContext) -> None:
        super().__init__(context)
    
    def _execute(self, load_result:dict) -> None:
         with self.out_stream() as dest:
            load_result['params'] = self.context.parameters
            json.dump(load_result, dest)

