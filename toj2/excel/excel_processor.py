import re
import pathlib
from ..processors import Jinja2Processor

class ExcelProsessor(Jinja2Processor):
    
    def execute(self, load_result):

        if self.context.split is None:
            # --split指定がない場合、一度で出力を終える
            self.execute_render(load_result)
            return

        dir = pathlib.Path(self.context.out)
        for idx, sheet in enumerate(load_result['sheets']):
            # シート枚数分複数回出力する、参照自体は毎回すべてのシートが参照可能
            load_result['current'] = {'idx': idx, 'sheet': sheet}
            # context.outは不可逆に変更される
            self.context.out = self.get_filename(idx, sheet, dir)
            self.execute_render(load_result)
        
    def execute_render(self, load_result:dict):
        """テストで補足しやすいように内部メソッドでexecuteする"""
        super().execute(load_result)

    def get_filename(self, idx:int, sheet:dict, dir:pathlib.Path):
        """1シート毎に出力を分ける場合にファイル名を生成する
        ファイル名は[連番3桁]_[シート名][suffix]
        suffixは引数--split-suffixで指定したものが使われる。
        シート名にファイルに使えない文字が含まれる場合、_に置換される。
        """
        name_body = re.sub(r'[ \\/*?:"<>|]', '_', sheet['name'])
        sheet_name = f"{str(idx).zfill(3)}_{name_body}{self.context.split}"
        return str(dir.joinpath(sheet_name))

