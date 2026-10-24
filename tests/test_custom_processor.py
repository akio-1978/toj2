import unittest
import sys
import contextlib
from toj2.runner import Runner
from tests.testutils import J2SRenderingTest

class CustomProcessorRunnerTest(J2SRenderingTest):

    def result_dir(self):
        """出力ディレクトリ名を返す"""
        return 'runner'

    def test_custom_processor_csv(self):
        """--processor（カスタムプロセッサ） CSV"""

        expect_file = self.expect_path(J2SRenderingTest.CUSTOM, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', '-', 'tests/csv/src/simple.csv', 
            result_file, '--processor', './tests/custom_processor/custom.py:SimpleCustomProcessor']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_custom_processor_excel(self):
        """--processor（カスタムプロセッサ） Excel"""
        
        expect_file = self.expect_path(J2SRenderingTest.CUSTOM, 'read_excel.txt')
        result_file = self.result_file()
        Runner(args=['excel', '-', 'tests/excel/src/multi.xlsx',
            '--processor', './tests/custom_processor/custom.py:ExcelCustomProcessor',
            result_file, '3:', 'A2:G', ]).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_custom_processor_json(self):
        """--processor（カスタムプロセッサ） Json"""

        Runner(args=['json', '-', 'tests/json/src/simple_json.json', 
            '-', '--processor', './tests/custom_processor/custom.py:JsonProcessor']).execute()

    def test_custom_processor_yaml(self):
        """--processor（カスタムプロセッサ） YAML"""

        Runner(args=['yaml', '-', 'tests/yaml/src/simple_yaml.yaml', 
            '-', '--processor', './tests/custom_processor/custom.py:JsonProcessor']).execute()

    def test_custom_processor_error(self):
        """--processor（カスタムプロセッサ） TypeError"""
        with self.assertRaises(TypeError):
            Runner(args=['yaml', '-', 'tests/yaml/src/simple_yaml.yaml', 
                '-', '--processor', './tests/custom_processor/custom.py:DummyProcessor']).execute()



if __name__ == '__main__':
    unittest.main()
