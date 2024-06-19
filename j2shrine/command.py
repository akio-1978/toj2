import io
import sys
import argparse
import json

from .render import Render
from .context import RenderContext
from .renderutils import get_stream, KeyValuesParseAction

# CommandRunnerのデフォルト実装


class Command():

    def __init__(self,*, factory: argparse.ArgumentParser):
        """このコンストラクタはテスト用で、何もしないサブコマンドを生成する"""
        self.parser = factory.add_parser('nop', help='NOP for test')
        factory.set_defaults(command_instance=self)

    def render_class(self):
        """Commandが使うRenderのクラスを返す"""
        return Render
    def context_class(self):
        """Commandが使うContextのクラスを返す"""
        return RenderContext

    def setup(self):
        """ コマンドの引数を定義する
            引数定義は3つのメソッドに分かれており、それぞれ個別にオーバーライドできる
        """
        self.add_default_options()
        self.add_positional_arguments()
        self.add_optional_arguments()

    def add_positional_arguments(self):
        """ 位置引数をパーサに追加する
            位置引数を書き直したい場合にオーバーライドする
            引数templateとsourceは必須のため、サブコマンドではsuper呼出しするのが好ましい
        """
        self.parser.add_argument('template', help='使用するjinja2テンプレート.')
        self.parser.add_argument('source', help='レンダリング対象ファイル 省略時はstdin.',
                            nargs='?', default=sys.stdin)

    def add_optional_arguments(self):
        """サブコマンドでオプションを追加する場合にこのメソッドをオーバーライドする"""
        pass

    def add_default_options(self):
        """ オプション引数をパーサに追加する
            全てのサブコマンドで共通して使うオプションを想定しているので
            オーバーライドは不要
        """
        self.parser.add_argument('-o', '--out', metavar='file',
                            help='出力先ファイル 省略時はstdout.', default=sys.stdout)
        # source encoding
        self.parser.add_argument('--input-encoding', metavar='enc',
                            help='入力時の文字エンコーディング.', default='utf-8')
        # dest encoding
        self.parser.add_argument('--output-encoding', metavar='enc',
                            help='出力時の文字エンコーディング.', default='utf-8')
        # template encoding
        self.parser.add_argument('--template-encoding', metavar='enc',
                            help='jinja2テンプレートファイルのエンコーディング.', default='utf-8')
        self.parser.add_argument('-p', '--parameters', nargs='*', default={},
                            help='テンプレート内で参照可能な追加のパラメータ [KEY=VALUE] 形式で列挙.', action=KeyValuesParseAction)

        self.parser.add_argument('-n', '--names', nargs='*',
                            help='テンプレート内で各行のカラムに付ける名前を左側から列挙 defaultは col_00 col02...')

        self.parser.add_argument('--config-file', metavar='file',
                            help='names parameters absoluteの各設定をjsonに記述したファイル')


    def execute(self, *, args: argparse.Namespace):
        """ パーサから返された値を使ってコマンドの処理を実行
        """
        # context及びrenderのクラスを取得
        ctx_class = self.context_class()
        render_class = self.render_class()

        # context及びrenderのインスタンスを生成
        context = ctx_class(args=Config().configure(args=args))
        render = render_class(context=context)
        
        # レンダリング実行
        self.call_render(render=render, source=args.source, out=args.out)

    def call_render(self, *, render: Render, source:str | io.TextIOWrapper, out:str | io.TextIOWrapper):
        context = render.context
        # sourceはファイル名かstdin/stdoutなので間にwrapperを挟む
        with get_stream(source=source,encoding=context.input_encoding) as src:
            with get_stream(source=out,encoding=context.output_encoding, mode='w') as dest:
                render.render(source=src, output=dest)

class Config:
        
    def configure(self, args:argparse.Namespace):
        """ コマンドライン引数(argparse.Namespace)と設定ファイル(json)の内容を統合する
            設定ファイルはコマンドラインからオプション'config_file'で指定される。設定ファイルがなければ何もしない。
            両者の間で設定が重複する場合、コマンドラインを優先する
            ただし、設定値がdictの場合、コマンドラインを優先しつつ設定ファイルの値をマージする
        """
        # 設定ファイルがなければ何もしない
        if self.given(args, 'config_file'):
            config = {}
            with open(args.config_file) as src:
                config.update(json.load(src))

            # 設定ファイルの中身を順次argsに反映する
            for key, value in config.items():
                if isinstance(value, dict):
                    # dict型の場合はマージする（コマンドラインが優先）
                    value.update(getattr(args, key))
                    setattr(args, key, value)
                elif (not self.given(args, key)):
                    # コマンドラインから設定されていなければ、設定ファイルの値を採用する
                    setattr(args, key, value)
        return args

    def given(self, args:argparse.Namespace, k:str):
        """ 属性が存在しないか、値がNoneではない """
        return hasattr(args, k) and getattr(args, k)

        
        