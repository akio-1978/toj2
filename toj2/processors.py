import pathlib
from jinja2 import Environment, FileSystemLoader
from .context import AppContext
from .jinja2_custom_filter import sequential_group_by
from .excel.excel_custom_filter import excel_time
from .utils import get_stream
class Processor:
    def __init__(self, context:AppContext) -> None:
        self.context = context
        self._setup()
        self.output_func = None

    # 読み取り結果を渡すオブジェクトを指定する
    # メソッドの引数は(load_object:dict, context:AppContext)であること
    def set_output_func(self, output_func: callable):
        self.output_func = output_func

    def _setup (self):
        pass

    def execute(self, load_result:dict):
        if (self.output_func is None):
            self._execute(load_result)
        else:
            self.output_func(load_result, self.context)

    def _execute(self, load_result):
        pass


class Jinja2Processor(Processor):
    def __init__(self, context:AppContext) -> None:
        super().__init__(context)
    
    def _setup(self):
        """jinja2テンプレート生成"""
        path = pathlib.Path(self.context.template)
        environment = Environment(loader=FileSystemLoader(
            path.parent, encoding=self.context.template_encoding))
        self._install_filters(environment=environment)
        self.template = environment.get_template(path.name)

    def _install_filters(self, environment):
        """追加のフィルタを設定する"""
        environment.filters['sequential_group_by'] = sequential_group_by
        environment.filters['excel_time'] = excel_time

    def _execute(self, load_result:dict):
        with get_stream(source = self.context.out ,mode = 'w', 
                            encoding = self.context.output_encoding,
                        ) as dest:
            load_result['params'] = self.context.parameters
            dest.write(self.template.render(load_result))

