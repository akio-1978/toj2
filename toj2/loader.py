from .jinja2_custom_filter import sequential_group_by
from .processors import Processor
from .context import AppContext

class Loader:

    def __init__(self, *, context : AppContext, processor : Processor) -> None:
        self.context = context
        self.processor = processor

    def execute(self) -> None:
        self.processor.execute(self.loading())

    def loading(self) -> dict:
        return None

    # カラム名取得
    # cols属性がないとこのメソッドは動かない
    def get_name(self, index: int) -> str:
        if len(self.cols) <= index:
            # カラム名が定義されていない場合
            # または定義済みのカラム名よりも実際のカラムが多い場合はカラム名を追加で生成する
            self.cols.append(self.context.col_prefix + str(index).zfill(2))
        return self.cols[index]
