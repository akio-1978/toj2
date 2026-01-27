import sys
import argparse
import json
import toj2
from .command import Command
from .csv.csv_command import CsvCommand
from .excel.excel_command import ExcelCommand
from .json.json_command import JsonCommand
from .yaml.yaml_command import YamlCommand
from .context import AppContext


class Runner():
    """コマンドラインから呼び出される処理の起点となるクラス"""

    def __init__(self, *, args:list) -> None:
        self.args = args
        self.PARSER_CMD = {
            'csv' : CsvCommand,
            'excel' : ExcelCommand,
            'json' : JsonCommand,
            'yaml' : YamlCommand
        }

    def execute(self) -> None:
        """プログラム実行"""
        # ファイル形式に対応した実際のコマンドを取得する
        # contextには設定ファイルの中身が書き込まれている
        command, context = self.build_cmd(args=self.args)

        # ファイル形式に対応した実際のコマンドを実行する
        # コマンドライン入力は内部で再度parseされ、結果はcontextに書き込まれる
        # ※contextはImmutableではない
        command.execute(args=self.args, context=context)

    def build_cmd(self, *, args:list) -> Command:
        """引数を一部だけパースしてcontextとcommandを取得する"""
        # サブコマンドと設定ファイルだけを取得する、サブコマンドが対象外の場合ここで終了する
        ctx_parser = CustomHelpParser(prog=toj2.PROG_NAME, add_help=False)
        ctx_parser.add_argument('cmd', choices=['csv', 'excel', 'json'], default='')
        ctx_parser.add_argument('--config-file', default=None)
        parsed, unknown = ctx_parser.parse_known_args(args)

        # コマンドからコンテキストの取得
        context = AppContext()
        if parsed.config_file:
            # 設定ファイルが存在すればコンテキストに書き込む
            self.load_config_file(context=context, filename=parsed.config_file)
        return self.get_cmd_instance(cmd_type=parsed.cmd), context

    def load_config_file(self,*, context: AppContext, filename: str) -> AppContext:
        """ 設定ファイルの内容をcontextにsetattrする"""
        with open(filename) as src:
            config = json.load(src)
            # 設定ファイルの中身を順次argsに反映する
            for key, value in config.items():
                setattr(context, key, value)
        return context

    def get_cmd_instance(self, *, cmd_type:str):
        """ Commandクラスインスタンスの取得 """
        return self.PARSER_CMD[cmd_type]()

class CustomHelpParser(argparse.ArgumentParser):
    
    def format_usage(self) -> str:
        """一回目の予備パースでエラーが出た時、config-fileオプションについて表示しない"""
        return f'usage: {toj2.PROG_NAME} [-h] {{csv,excel,json}} ...\n'

def main():
    """sys.argvをargparseに直接渡さない（Ruunerのテスト対策）"""
    starter = Runner(args=sys.argv[1:] if len(sys.argv) > 1 else ['', ''])
    starter.execute()

if __name__ == '__main__':
    main()
