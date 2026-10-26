[トップへ](../README.md)
# カスタムプロセッサ
toj2のカスタムプロセッサ機能についての解説です。

## カスタムプロセッサとは
カスタムプロセッサとは、toj2が読み込んだデータをjinja2の代わりに処理する **ユーザ定義のpythonクラスのことをそう呼んでいます。**
コマンドにカスタムプロセッサを指定すると、toj2はjinja2を起動せず、入力ファイルの読み取り結果をそのままpythonクラスのメソッド引数として引き渡します。

カスタムプロセッサを使うと入力を自由に処理できます。 **出力を行わずに別の処理をさせることさえ可能です。**

### カスタムプロセッサ指定コマンド
カスタムプロセッサを使用する最小のコマンドラインは以下です。
```
toj2 - in.csv out.txt --processor ./custom.py:MyCustomProcessor
```
- 第一引数のテンプレート名は無視されるので`-`を指定しています。[^template-name]
- オプション`--processsor`の後に`[pythonファイル名:クラス名]`の形式で使用するプロセッサを指定します。

`--processor`オプションは`--dump`オプションと矛盾する関係にあるため、`--processor`と`--dump`の両方を指定すると **`--dump`オプションが優先されます。**

### カスタムプロセッサの作成
カスタムプロセッサを作成するには、toj2のクラス`Processor`をオーバーライドしたクラスを作成します。[^invalid-class]、オーバーライドするメソッドを以下に示します。

```
from toj2.processors import Processor

class MyCustomProcessor(Processor):

    def _setup (self):
        pass

    def _execute(self, result) -> None:
        pass

```
- `_setup`はデータの読込み前に呼び出されます。変換の前処理を行うことができます。
- `_execute`はデータの読込み後に読込みデータと共に呼び出されます。 **toj2はexecuteメソッドの呼び出しが終わった後に処理を終了します。プログラムに終了処理が必要な場合、executeメソッド内で行う必要があります。**

### 引数コンテキスト
toj2コマンドに渡された全てのコマンドライン引数及び設定ファイルの値は`self.context`から参照できます。位置引数は先頭から以下の名前です。[^setup]
- template テンプレートファイル名
- src 入力ファイル名
- out 出力ファイル名
オプション引数については、例えば`--input-encoding`は`self.context.input_encoding`等のように変換されます。複数指定可能な値は`list`で、`KEY=VALUE`形式のものは`dict`で表現されます（しかし、引数`--parameters`の内容は`_execute`メソッドの引数`result`に含まれています）。

**作成したカスタムプロセッサに固有の引数が必要な場合、引数`--parameters`を用いて渡すことができます。**

### _executeメソッドへの入力例
各ファイル形式のチュートリアルで説明した再掲ですが、例えばcsvファイルの場合 `result`の中身は以下のような`dict`です。
```python
{
    'cols' : ['col_00','col_01','col_02'], # csvカラム名のリスト、デフォルトは連番です
    'rows' : [ # csvの各行の内容を含んだリスト

        {   # csvの1行ごとにdictが生成されます
            # カラム名はリスト cols に格納された文字列です。データは全て文字列として扱われます。
            'col_00' : '1',
            'col_01' : '佐藤 はじめ',
            'col_02' : 'サッカー部'
        },
        # 以下略
    ],
    'params' : { # コマンド引数 --parameters で渡された値はここに格納されます
        'title' : '部活別生徒リスト'
    }                       
}
```

[^template-name]: テンプレート名に指定された値を確認することはできます。
[^invalid-class]: コマンドに渡されたクラスがProcessorクラスのサブクラスでない場合、TyprErrorが送出されます。
[^setup]: `_setup`メソッド呼び出し時点で`self.context`は設定済みです。


