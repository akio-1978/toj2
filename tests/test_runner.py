import unittest
from j2shrine.runner import Runner
from tests.testutils import J2SRenderTest

# テスト用のファイルパスが長たらしいのでヘルパー
CSV = 'csv'
EXCEL = 'excel'
EXPECT = 'tests/{}/expect/{}'
RESULT = 'tests/output/{}/{}'
def expect_path(type, file):
    return EXPECT.format(type, file)
def result_path(type, file):
    return RESULT.format(type, file)
class RunnerTest(J2SRenderTest):

    def test_start(self):
        """最低限の引数で起動"""
        expect_file = expect_path(CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/simple.tmpl', 'tests/csv/src/simple.csv', 
            '-o', result_file, '-H']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_start_jp(self):
        """日本語読み書き"""
        expect_file = expect_path(CSV, 'simple_sjis.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/simple.tmpl', 'tests/csv/src/simple_sjis.csv', 
            '-o', result_file, '-H', '--input-encoding', 'sjis', '--output-encoding', 'sjis']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file, encoding='sjis')


    def test_start_args(self):
        """オプション引数を指定して起動"""
        expect_file = expect_path(CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/simple.tmpl', 'tests/csv/src/simple.csv',
            '-o', result_file, '-H', '--input-encoding', 'utf8', '--output-encoding', 'utf8',
            '-d',',', '-p' ,'A=B', 'C=D']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)


    def test_header_names(self):
        """--headerと--namesを同時に指定した場合はheaderを優先する"""
        expect_file = expect_path(CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/use_column_names.tmpl', 'tests/csv/src/simple.csv', 
            '-o', result_file, '-H', '--names', 'not', 'use', 'names', ]).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_start_names(self):
        """--names指定で起動"""
        expect_file = expect_path(CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/use_column_names.tmpl', 'tests/csv/src/simple.csv', 
            '-o', result_file, '-s', '1', '--names', 'group', 'number', 'name']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_start_names_short(self):
        """-n 指定で起動"""
        expect_file = expect_path(CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/use_column_names.tmpl', 'tests/csv/src/simple.csv', 
            '-o', result_file, '-s', '1', '-n', 'group', 'number', 'name']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_start_excel(self):
        """Excel変換起動（引数が複雑）"""
        expect_file = expect_path(EXCEL, 'read_document.txt')
        result_file = self.result_file()
        Runner(args=['excel', 'tests/excel/templates/read_document.tmpl', 'tests/excel/src/read_document.xlsx',
            '1:', 'C7:H10', '-o', result_file, '--absolute', 'NAME=C3', 'DESCRIPTION=C4']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_excel_demo(self):
        """同じソースを複数回レンダリングするデモ"""
        expect_file = expect_path(EXCEL, 'demo01.sql.txt')
        result_file = self.result_file('demo01')
        Runner(args=['excel', 'tests/excel/templates/read_demo01.tmpl', 'tests/excel/src/read_demo.xlsx',
            '1:', 'A6:G', '-o', result_file, '--absolute', 'TABLE=C3', 'LABEL=C4']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

        expect_file = expect_path(EXCEL, 'demo02.html.txt')
        result_file = self.result_file('demo02')
        Runner(args=['excel', 'tests/excel/templates/read_demo02.tmpl', 'tests/excel/src/read_demo.xlsx',
            '1:', 'A6:G', '-o', result_file, '--absolute', 'TABLE=C3', 'LABEL=C4']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_csv_help(self):
        starter = Runner(args=['csv', '-h'])
        self.assertRaises(BaseException, starter.execute)

    def test_excel_help(self):
        starter = Runner(args=['excel', '-h'])
        self.assertRaises(BaseException, starter.execute)

    def test_json_help(self):
        starter = Runner(args=['json', '-h'])
        self.assertRaises(BaseException, starter.execute)

    def test_csv_invalid(self):
        starter = Runner(args=['csv'])
        self.assertRaises(BaseException, starter.execute)

    def result_dir(self):
        return 'starter'

if __name__ == '__main__':
    unittest.main()