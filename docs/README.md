# toj2

## これは何ですか？
csvやexcelをjinja2テンプレートで処理できるツールです。

## 使用方法 使用例
ファイル変換の例を紹介します。
### csvファイルを変換方法
[toj2によるCSVファイル変換](./csv/csv-tutorial.md)

### excelファイルの変換方法
[toj2によるExcelファイル変換](./excel/excel-tutorial.md)

### json/yamlファイルを変換する例
[json/yamlについてはごくシンプルな動作のみ](JSONファイルの変換)なので、jsonのみこのファイル内で解説します。

## 動作条件
#### pythonバージョン
pytthon3.13で開発しています。
#### インストール
PyPIには上げないので、このリポジトリから直接取得してください。
```sh
pip install git+https://github.com/akio-1978/toj2
```
#### 依存関係
以下の外部モジュールを使用しています。
- jinja2
- openpyxl
- pyyaml

## 実行方法
コマンドとして実行します。例えば以下のような形になります。

```sh
toj2 csv demo.tmpl demo.csv test.out
```

## 共通コマンド引数
引数には変換するファイル形式に応じた固有の引数がありますが、ここでは全てのファイル形式に共通した引数について解説します。
[CSVファイル固有の引数はこちら](./csv/csv-tutorial.md)  |  [Excelファイル固有の引数はこちら](./excel/excel-tutorial.md) [^except-excel]

### 位置引数
記述位置で意味が決まる引数です。
位置引数だけ指定してtoj2を実行すると以下のようなイメージになります。

```sh
toj2 csv demo.tmpl demo.csv test.out
```

#### 処理データ種別
指定必須です。以下のいずれかから処理対象のファイルを指定します。
- csv
- excel
- json
- yaml

値がexcelの場合は位置引数にも変化があるので、[excel変換仕様](./excel/excel-tutorial.md)を確認してください。

#### jinja2テンプレートファイル
指定必須です。実行されるjinja2テンプレートファイルを指定します。
**jinja2のFileSystemLoaderにはこのファイルが配置されたディレクトリが指定されます。** ここを基準に他のテンプレートのinclude等が行えます。

#### 変換対象ファイル
指定必須です。変換元として読み込むファイルを指定します。
ファイル名の代わりに`-`を指定するとtoj2は標準入力から変換対象を受け取ります。
*最終更新 バージョン 0.3.0*

#### out 出力ファイル
指定必須です。変換結果を出力するファイルを指定します。
ファイル名の代わりに`-`を指定するとtoj2は変換結果を標準出力に出力します。
*最終更新 バージョン 0.3.0*

### オプション引数
すべてのデータ形式で設定可能なオプション引数です。

#### --input-encoding --output-encoding 文字列エンコーディング

`--input-encoding enc`
`--output-encoding enc`

入出力ファイルのエンコーディングを指定します。デフォルトはUTF8です。**excelでは`--input-encoding`は無視されます。**

#### --parameter テンプレートパラメータ
jinja2テンプレートに任意の値を渡すことができます。値は`=`でキーと値に区切って指定します。指定できる数に制限はありません。

`--parameter PARAM1=A PARAM2=B `

この値は、テンプレート中で`param.PARAM1`のようにして参照できます。

#### --config-file 設定ファイル
ときどき、toj2の引数が長いものになることがあります。そのような場合、オプション引数をjsonにまとめることができます。

以下のようなコマンドが少し長いと感じるでしょう（以下はcsv変換用のオプションを含みます）。

```sh
toj2 csv sample.tmpl sample.csv test.out --skip-lines 1 --names one two three four --parameters PARAM1=A PARAM2=B PARAM3=C
```

このオプションを以下のような`config.json`としてまとめて記述します。設定ファイル内ではオプション名の先頭のふたつのハイフンは除去し、途中に現れるハイフンはアンダースコアに置き換えます。

```json
{
  "skip_lines": 1,
  "names": ["one", "two", "three", "four"],
  "parameters": {
      "PARAM1" : "A",
      "PARAM2" : "B",
      "PARAM3" : "C"
  }
}
```

そして、コマンドを以下のように実行すると、`config.json`の内容がオプションとして使用されます。
```sh
toj2 csv sample.tmpl sample.csv test.out --config-file config.json
```

これだけではなく、**設定ファイルはコマンドラインからオーバーライドすることができます。**
```sh
toj2 csv sample.tmpl sample.csv test.out --config-file config.json --skip-lines 0 --parameters PARAM1=X PARAM4=D
```
設定ファイル中の`skip-lines`は`1`ですが、ここでは`0`に置き換わります。

`--parameters`オプションのうち、パラメータ`PARAM1`の値は`X`に変更され、新たに`PARAM4`が追加されますが**`PARAM2`と`PARAM3`は影響を受けません。**設定ファイル内で値またはリストで記述するものは置き換えられ、オブジェクトで記述されるものはマージされます。**常にコマンドラインからの設定が優先して採用されます。

### JSON/YAMLファイルの変換
JSON/YAMLの処理については特に固有のオプションはなく、共通オプションのみが使用できます。

```sh
toj2 json jsontemplate.tmpl data.json test.out
toj2 yaml yamltemplate.tmpl data.yaml test.out
```

#### jinja2への出力形式
toj2はJSON/YAMLを以下の形式にしてjinja2に渡します。
JSONは標準の`json.load`、YAMLはpyyamlの`yaml.safe_load`で読み込んだ内容を`data`に格納する以外何もしません。
```python
{
    # 受け取ったjsonをjson.loadした結果
    'data': {},
    # 起動時に渡したパラメータ
    'params' : {'PARAM' : 'VALUE'}
}

```

[^except-excel]: Excel変換はこの形式に合致しない例外が多いので、別途確認してください。
