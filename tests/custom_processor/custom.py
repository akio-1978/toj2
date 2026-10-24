from toj2.processors import Processor
from toj2.utils import get_stream

class SimpleCustomProcessor(Processor):
    
    def _execute(self, result) -> None:
        with self.out_stream() as dest:
            for row in result['rows']:
                print(f'{row["col_02"]}/{row["col_01"]}/{row["col_00"]}', file=dest)

class ExcelCustomProcessor(Processor):
    def _execute(self, result):
        with self.out_stream() as dest:
            for sheet in result["sheets"]:
                print(f'<{sheet['name']}>', file=dest)
                for row in sheet['rows']:
                    print(f'{row["col_00"]}>{row["col_01"]}>{row["col_02"]}>{row["col_03"]}>{row["col_04"]}>', file=dest)
        
