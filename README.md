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
