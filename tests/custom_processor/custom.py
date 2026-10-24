import json
from toj2.processors import Processor
from toj2.utils import get_stream

class SimpleCustomProcessor(Processor):
    """csv用プロセッサ"""    
    def _execute(self, result) -> None:
        with self.out_stream() as dest:
            for row in result['rows']:
                print(f'{row["col_02"]}/{row["col_01"]}/{row["col_00"]}', file=dest)

class ExcelCustomProcessor(Processor):
    """excel用プロセッサ 複数シート読込み"""
    def _execute(self, result):
        with self.out_stream() as dest:
            for sheet in result["sheets"]:
                print(f'<{sheet['name']}>', file=dest)
                for row in sheet['rows']:
                    print(f'{row["col_00"]}>{row["col_01"]}>{row["col_02"]}>{row["col_03"]}>{row["col_04"]}>', file=dest)
        
class JsonProcessor(Processor):
    """何もしないプロセッサ json/yaml用"""
    def _execute(self, result) -> None:
        """結果が解りきっているのでdumpできればOK"""
        json.dumps(result)

class DummyProcessor():
    """プロセッサを継承していないクラス、TyprErrorになる"""
    pass