import io
import sys
from pathlib import Path
from jinja2 import Template, Environment, FileSystemLoader

class CsvTransformer:

    # jinja2テンプレートの生成
    def __init__(self, *, template):
        path = Path(template)
        self.loader_directory = path.parent
        self.template_file = path.name
        environment = Environment(loader = FileSystemLoader(self.loader_directory, encoding='utf-8'))
        self.template = environment.get_template(self.template_file)

    # CSVファイルの各行にテンプレートを適用して、出力する
    def transform(self, *, file):
        lines = []
        with open(file, 'r', encoding='utf-8') as source:
            for line in source:
                lines.append(self.transform_columns(columns = self.parse_tokens(line = line)))
        print(
            self.template.render(
                {'lines' : lines}
            )
        )

    # 以下はオーバーライドできるようにメソッドを細かく分けた

    # 行をカラムに分解
    def parse_tokens(self, *, line):
        # 今回は単純なsplitを使う
        # エスケープの必要なcsvはテンプレートの適用も大変なので、単純に
        return line.split(',')

    # 1行分の分解されたカラムを処理する
    def transform_columns(self, *, columns):
        line_no = 0
        result = {}
        for column in columns:
            column_name = self.column_name(column_no = line_no)
            result[column_name] = self.column(token = column)
            line_no = line_no + 1
        return self.transformed_line(result = result)

    # CSVのカラムに名前を付ける
    # このカラム名がテンプレートから参照される
    def column_name(self, *, column_no):
        # 'column_01'とかの文字列
        return 'column_' + str(column_no).zfill(2)

    # 分解されたひとつのカラムの処理
    def column(self, *, token, line_no=None, column_name=None):
        # stripだけ
        return token.strip()

    # 1行分の処理結果
    def transformed_line(self, *, result):
        # 今回はそのまま返す
        return result


if __name__ == '__main__':
    # windows対策
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    template_file = sys.argv[1]
    format_changer = CsvTransformer(template = template_file)
    format_changer.transform(file = sys.argv[2])
