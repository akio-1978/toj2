import unittest
import sys
import contextlib
from toj2.runner import Runner
from tests.testutils import J2SRenderingTest

class RunnerTest(J2SRenderingTest):

    def result_dir(self):
        """出力ディレクトリ名を返す"""
        return 'runner'

    def test_start(self):
        """最低限の引数で起動"""
        expect_file = self.expect_path(J2SRenderingTest.CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/simple.tmpl', 'tests/csv/src/simple.csv', 
            result_file, '-H']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_start_jp(self):
        """日本語読み書き"""
        expect_file = self.expect_path(J2SRenderingTest.CSV, 'simple_sjis.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/simple.tmpl', 'tests/csv/src/simple_sjis.csv', 
            result_file, '-H', '--input-encoding', 'sjis', '--output-encoding', 'sjis']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file, encoding='sjis')


    def test_start_args(self):
        """オプション引数を指定して起動"""
        expect_file = self.expect_path(J2SRenderingTest.CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/simple.tmpl', 'tests/csv/src/simple.csv',
            result_file, '-H', '--input-encoding', 'utf8', '--output-encoding', 'utf8',
            '-d',',', '-p' ,'A=B', 'C=D']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)


    def test_header_names(self):
        """--headerと--namesを同時に指定した場合はheaderを優先する"""
        expect_file = self.expect_path(J2SRenderingTest.CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/use_column_names.tmpl', 'tests/csv/src/simple.csv', 
            result_file, '-H', '--names', 'not', 'use', 'names', ]).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_start_names(self):
        """--names指定で起動"""
        expect_file = self.expect_path(J2SRenderingTest.CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/use_column_names.tmpl', 'tests/csv/src/simple.csv', 
            result_file, '-s', '1', '--names', 'group', 'number', 'name']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_start_names_short(self):
        """-n 指定で起動"""
        expect_file = self.expect_path(J2SRenderingTest.CSV, 'simple.txt')
        result_file = self.result_file()
        Runner(args=['csv', 'tests/csv/templates/use_column_names.tmpl', 'tests/csv/src/simple.csv', 
            result_file, '-s', '1', '-n', 'group', 'number', 'name']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_start_excel(self):
        """Excel変換起動（引数が複雑）"""
        expect_file = self.expect_path(J2SRenderingTest.EXCEL, 'read_document.txt')
        result_file = self.result_file()
        Runner(args=['excel', 'tests/excel/templates/read_document.tmpl', 'tests/excel/src/read_document.xlsx',
            result_file, '1:', 'C7:H10', '--absolute', 'NAME=C3', 'DESCRIPTION=C4']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_excel_demo(self):
        """同じソースを複数回レンダリングするデモ"""
        expect_file = self.expect_path(J2SRenderingTest.EXCEL, 'demo01.sql.txt')
        result_file = self.result_file('demo01')
        Runner(args=['excel', 'tests/excel/templates/read_demo01.tmpl', 'tests/excel/src/read_demo.xlsx',
            result_file, '1:', 'A6:G', '--absolute', 'TABLE=C3', 'LABEL=C4']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

        expect_file = self.expect_path(J2SRenderingTest.EXCEL, 'demo02.html.txt')
        result_file = self.result_file('demo02')
        Runner(args=['excel', 'tests/excel/templates/read_demo02.tmpl', 'tests/excel/src/read_demo.xlsx',
            result_file, '1:', 'A6:G', '--absolute', 'TABLE=C3', 'LABEL=C4']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_split_sheets_loss_suffix(self):
        """--splitの引数不正（suffix未指定）"""
        result_file = self.result_file()
        with self.assertRaises(BaseException):
            Runner(args=['excel', 'tests/excel/templates/read_document.tmpl', 'tests/excel/src/read_document.xlsx',
                result_file, '1:', 'C7:H10', '--split', '--absolute', 'NAME=C3', 'DESCRIPTION=C4']).execute()

    def test_split_omit_suffix(self):
        """--split（--splitにディレクトリを指定しない）"""

        with self.assertRaises(ValueError):
            Runner(args=['excel', 'tests/excel/templates/simple.tmpl', 'tests/excel/src/simple.xlsx',
                'tests/excel/templates/simple.tmpl', '1', 'A2:A5', '--split', 'outtodir']).execute()
            self.file_test(expect_file='tests/excel/expect/000_Sheet1', result_file='tests/output/excel/000_Sheet1')

    def test_stdio(self):
        """stdio入出力"""
        expect_file = self.expect_path(J2SRenderingTest.CSV, 'simple.txt')
        result_file = self.result_file()
        with self.redirect_stdin(open('tests/csv/src/simple.csv')):
            with contextlib.redirect_stdout(open(result_file, mode='w')):
                Runner(args=['csv', 'tests/csv/templates/simple.tmpl', '-', 
                    '-', '-H']).execute()
        self.file_test(expect_file=expect_file, result_file=result_file)

    def test_excel_stdio_error(self):
        """excelの入力にstdinは使えない"""

        with self.assertRaises(ValueError):
            Runner(args=['excel', 'tests/excel/templates/simple.tmpl', '-',
                'tests/excel/templates/simple.tmpl', '1', 'A2:A5', '--split', 'outtodir']).execute()
            self.file_test(expect_file='tests/excel/expect/000_Sheet1', result_file='tests/output/excel/000_Sheet1')


    @contextlib.contextmanager
    def redirect_stdin(self, new_stdin):
        old = sys.stdin
        sys.stdin = new_stdin
        try:
            yield
        finally:
            sys.stdin = old


if __name__ == '__main__':
    unittest.main()
