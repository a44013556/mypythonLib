baseModel.py
特徴：
  Datebase Agnostic:特定のデータベースに依存せず、任意のエンジンを注入可能。
  
  Lightweight:外部ライブラリへの依存がなく、非常に軽量。
  
  Type Safe:PythonのType Hintingをフル活用し、開発時の安心感を提供。
  
使い方：
  1. データベースエンジンの実装 (Implement Engine)
  `IDatabaseEngine` を継承して、既存のデータベース接続ロジックをラップします。

  2. エンジンのセットアップ (Setup)
  アプリケーションの起動時にエンジンを登録します。
  BaseModel.set_engine(YourCustomEngine())

baseCsvReader.py
特徴：
  Smart Encoding Detection:
    utf-8, shift_jis, cp932 などの主要なエンコーディングを自動的に試行・判別します。日本語を含むCSVファイルの読み込みで頻発する文字化け問題を、外部ライブラリなしで解決します。
  
  Built-in Type Casting:
    field_types に辞書形式で関数を指定するだけで、CSVの文字列データを int, float, bool などの適切な型へ自動変換します。

  Header Flexibility:
    ヘッダーの有無を選択できるだけでなく、ヘッダーがないファイルに対しては自動的に column_1 のような仮のヘッダーを付与して構造化します。

  Robust Reading:
    デコードに失敗した場合のフォールバック処理や、型変換に失敗した際の None 代入処理を内蔵しており、データ不備によるプログラム停止を最小限に抑えます。
  
使い方：
  1. リーダーの実装 (Implement Reader)
   BaseCsvReader を継承し、読み込みたいCSVの構造（型）を定義します。

  2. エンジンのセットアップ (Setup)
    インスタンスを生成して read_all() を呼び出すだけで、型変換済みの辞書リストが取得可能です。
