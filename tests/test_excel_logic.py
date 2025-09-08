import unittest
import pathlib
from toj2.context import AppContext
from toj2.excel.excel_processor import ExcelProsessor

class ExcelLogicTest(unittest.TestCase):
    """
        ExcelFileTestが長くなりすぎたので分離する。
        ExcelFileTestではファイルを使ったテストを主に扱い、こちらは内部ロジックのテストに集中する
        --split-suffixがNoneの場合のテストはExcelFileTestで代替する
    """

    def test_split_one(self):
        """1シートを--sprit-suffix指定で出力する"""
        loaded = {'sheets' :[{'name': 'sheet_1'}]}
        context = AppContext()
        context.split_suffix = '.file'
        context.out = 'file/output'
        processor = ExcelProcessorForTest(context)
        processor.execute(loaded)
        self.assertEqual(1, processor.execute_called)
        self.assertEqual(1, len(processor.current_list))
        self.current_check(processor.current_list[0],
                           'file/output/000_sheet_1.file', 0, 'sheet_1')

    def test_split_three(self):
        """3シートを--sprit-suffix指定で出力する"""
        loaded = {'sheets' :[{'name': 'sheet_1'}, {'name': 'sheet_2'}, {'name': 'sheet_3'}]}
        context = AppContext()
        context.split_suffix = '.file'
        context.out = 'file/output'
        processor = ExcelProcessorForTest(context)
        processor.execute(loaded)
        self.assertEqual(3, processor.execute_called)
        self.assertEqual(3, len(processor.current_list))
        self.current_check(processor.current_list[0],
                           'file/output/000_sheet_1.file', 0, 'sheet_1')
        self.current_check(processor.current_list[1],
                           'file/output/001_sheet_2.file', 1, 'sheet_2')
        self.current_check(processor.current_list[2],
                           'file/output/002_sheet_3.file', 2, 'sheet_3')

    def test_split_escape_name(self):
        """
            シート名に含まれるファイルに使用できない文字を'_'に変換する
            半角スペースはファイル名に使用可能だが、紛らわしくなるのでこれも変換
        """
        loaded = {'sheets' :[{'name': 'escaped \\/*?:"<>|sheet'}]}
        context = AppContext()
        context.split_suffix = '.file'
        context.out = 'file/output'
        processor = ExcelProcessorForTest(context)
        processor.execute(loaded)
        self.assertEqual(1, processor.execute_called)
        self.assertEqual(1, len(processor.current_list))
        self.current_check(processor.current_list[0],
                           'file/output/000_escaped__________sheet.file', 0, 'escaped \\/*?:"<>|sheet')

    def current_check(self, ret:dict, filename:str, idx:int, sheetname:str):
        self.assertEqual(str(pathlib.Path(filename)), ret['filename'])
        self.assertEqual(idx, ret['idx'])
        self.assertEqual(sheetname, ret['name'])


class ExcelProcessorForTest(ExcelProsessor):

    def __init__(self, context:AppContext):
        self.context = context
        self.current_list = []
        self.execute_called = 0

    def _setup(self):
        pass

    def execute_render(self, loaded_object:dict):
        """呼び出し回数をカウントして、currentがある場合は記録する"""
        self.execute_called += 1
        if 'current' in loaded_object:
            # 結果判定用dict
            self.current_list.append({
                'filename' : self.context.out,
                'idx' : loaded_object['current']['idx'],
                'name' : loaded_object['current']['sheet']['name'],
                })
