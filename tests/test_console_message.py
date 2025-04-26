import unittest
from toj2.runner import Runner
from tests.testutils import J2SRenderingTest

class ConsoleTest(J2SRenderingTest):
    """コマンドラインの不正確な引数及びヘルプ表示、このテストは例外が発生すればok"""

    def test_no_subcommand(self):
        """サブコマンドの指定がない"""
        with self.assertRaises(SystemExit):
            Runner(args=[]).execute()

    def test_csv_no_arg(self):
        """csv 引数指定がない"""
        with self.assertRaises(SystemExit):
            Runner(args=['csv']).execute()

    def test_excel_no_arg(self):
        """excel 引数指定がない"""
        with self.assertRaises(SystemExit):
            Runner(args=['excel']).execute()

    def test_json_no_arg(self):
        """json 引数指定がない"""
        with self.assertRaises(SystemExit):
            Runner(args=['json']).execute()

    def test_csv_help(self):
        """csv ヘルプ表示"""
        with self.assertRaises(SystemExit):
            Runner(args=['csv', '-h']).execute()

    def test_excel_help(self):
        """excel ヘルプ表示"""
        with self.assertRaises(SystemExit):
            Runner(args=['excel', '-h']).execute()

    def test_json_help(self):
        """json ヘルプ表示"""
        with self.assertRaises(SystemExit):
            Runner(args=['json', '-h']).execute()

if __name__ == '__main__':
    unittest.main()
