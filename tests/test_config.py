import unittest
from j2shrine.runner import Runner
from utils import J2SRenderTest

# テスト用のファイルパスが長たらしいのでヘルパー
CSV = 'csv'
EXCEL = 'excel'
EXPECT = 'tests/{}/expect/{}'
RESULT = 'tests/output/{}/{}'
def expect_path(type, file):
    return EXPECT.format(type, file)
def result_path(type, file):
    return RESULT.format(type, file)
class ConfigTest(J2SRenderTest):

    def test_delimiter(self):
        """--delimiterを--config-fileから指定してタブ区切りにする"""
        expect_file = expect_path(CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/use_column_names.tmpl', 'tests/csv/src/simple_tab.tsv', 
            '-o', result_file, '--header', '--config-file', 'tests/csv/config/delimiter.json']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_skip_lines(self):
        """--skip-linesを--config-fileから指定する"""
        expect_file = expect_path(CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/use_column_names.tmpl', 'tests/csv/src/simple.csv', 
            '-o', result_file, '--names', 'group', 'number', 'name', '--config-file', 'tests/csv/config/skip_lines.json']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_names(self):
        """--namesの代わりに--config-fileを使ってカラム名を定義する"""
        expect_file = expect_path(CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/use_column_names.tmpl', 'tests/csv/src/simple.csv', 
            '-o', result_file, '-s', '1', '--config-file', 'tests/csv/config/names.json']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_overwrite_names(self):
        """--namesに指定した内容が--config-fileより優先して使用される"""
        expect_file = expect_path(CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/use_column_names.tmpl', 'tests/csv/src/simple.csv', 
            '-o', result_file, '-s', '1', '--names', 'group', 'number', 'name', '--config-file', 'tests/csv/config/overwrite.names.json']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_merge_parameter(self):
        """--parameters指定と--config-file中のparametersはマージされる"""
        expect_file = expect_path(CSV, 'merge_parameters.yml')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/merge_parameters.tmpl', 'tests/csv/src/parameters.csv', 
            '-o', result_file, '-H',
            '--parameters', 'list_name=Yurakucho-line-stations-in-ward', '--config-file', 'tests/csv/config/parameters.json', ]).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_overwrite_parameters(self):
        """--parameters指定は--config-fileより優先的にマージされる"""
        expect_file = expect_path(CSV, 'overwrite_parameters.yml')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/merge_parameters.tmpl', 'tests/csv/src/parameters.csv', 
            '-o', result_file, '-H',
            '--parameters', 'value2=overwrite', 'list_name=Yurakucho-line-stations-in-ward', '--config-file', 'tests/csv/config/parameters.json', ]).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_excel_absolute(self):
        """excel --absoluteを--config-fileから指定する"""
        expect_file = expect_path(EXCEL, 'read_document.txt')
        result_file = self.result_file()
        Runner(args=['excel', 'tests/excel/templates/read_document.tmpl', 'tests/excel/src/read_document.xlsx',
            '1:', 'C7:H10', '-o', result_file, '--config-file', 'tests/excel/config/absolute.json',]).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_excel_merge_absolute(self):
        """--absolute指定と--config-file中のabsoluteはマージされる"""
        expect_file = expect_path(EXCEL, 'read_document.txt')
        result_file = self.result_file()
        Runner(args=['excel', 'tests/excel/templates/read_document.tmpl', 'tests/excel/src/read_document.xlsx',
            '1:', 'C7:H10', '-o', result_file, '--absolute', 'DESCRIPTION=C4',
            '--config-file', 'tests/excel/config/merge_absolute.json',]).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)


    def test_excel_overwrite_absolute(self):
        """--absolute指定は--config-fileより優先的にマージされる"""
        expect_file = expect_path(EXCEL, 'read_document.txt')
        result_file = self.result_file()
        Runner(args=['excel', 'tests/excel/templates/read_document.tmpl', 'tests/excel/src/read_document.xlsx',
            '1:', 'C7:H10', '-o', result_file, '--absolute', 'NAME=C3', 'DESCRIPTION=C4',
            '--config-file', 'tests/excel/config/overwrite_absolute.json',]).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def result_dir(self):
        return 'config'

if __name__ == '__main__':
    unittest.main()
