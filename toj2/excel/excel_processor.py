import re
import pathlib
from ..loader import Loader
from ..context import AppContext
from ..processors import Jinja2Processor
from ..utils import get_stream

class ExcelProsessor(Jinja2Processor):
    
    def execute(self, loaded_object):

        if self.context.split is None:
            # --split指定がない場合、一度で出力を終える
            self.execute_render(loaded_object)
            return

        # contextの書き換えを行うが、outは再利用される可能性があるため、退避して後で戻す
        keep_path = self.context.out
        dir = pathlib.Path(self.context.out)
        for idx, sheet in enumerate(loaded_object['sheets']):
            # シート枚数分複数回出力する
            # 出力回数が分かれていても毎回すべてのシートが参照可能になっている
            loaded_object['current'] = {'idx': idx, 'sheet': sheet}
            self.context.out = self.get_filename(idx, sheet, dir)
            self.execute_render(loaded_object)
        # contextのoutを戻す
        self.context.out = keep_path
        
    def execute_render(self, loaded_object:dict):
        """テストで補足しやすいように内部メソッドでexecuteする"""
        super().execute(loaded_object)

    def get_filename(self, idx:int, sheet:dict, dir:pathlib.Path):
        """1シート毎に出力を分ける場合にファイル名を生成する
        ファイル名は[連番3桁]_[シート名][suffix]
        suffixは引数--split-suffixで指定したものが使われる。
        シート名にファイルに使えない文字が含まれる場合、_に置換される。
        """
        name_body = re.sub(r'[ \\/*?:"<>|]', '_', sheet['name'])
        sheet_name = f"{str(idx).zfill(3)}_{name_body}{self.context.split}"
        return str(dir.joinpath(sheet_name))

