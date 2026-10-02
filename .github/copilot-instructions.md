# Copilot への指示（プロジェクト規約）

このファイルは GitHub Copilot（VS Code の Copilot Chat / GitHub の Copilot coding agent）が
このリポジトリでコードやテストを生成するときに**自動で参照**する共通ルールです。

## このプロジェクトについて
- Python 製のショッピングカート価格計算ロジックのデモ。
- 本体コードは `src/cart/`、テストは `tests/` に置く。
- 技術発表会用なので、**読みやすさ・テストの網羅性**を最優先する。

## テストを書くときのルール
- テストフレームワークは **pytest** を使う。
- テストファイルは `tests/test_*.py`、テスト関数は `test_` で始める。
- **AAA パターン**（Arrange / Act / Assert）でブロックを分けてコメントを入れる。
- 複数の入力パターンは `@pytest.mark.parametrize` でまとめる。
- 以下の3観点を必ず網羅する:
  1. **正常系** — 代表的な入力で期待どおりの結果になること。
  2. **異常系** — 不正入力で `pytest.raises(ValueError)` など例外が出ること。
  3. **境界値** — 閾値ちょうど / 0 / 空リスト / 最小値などの境目。
- 金額計算は**端数処理（切り捨て）**の挙動までアサートする。
- テストの説明や関数名に日本語を使ってよい（例: `def test_送料無料の境界値():`）。

## コードを書くときのルール
- 公開関数には**型ヒント**と**docstring（Args/Returns/Raises）**を付ける。
- 副作用のない**純粋関数**を基本とする。
- Lint は **ruff**。`ruff check .` が通る状態を保つ（import整列・未使用変数なし）。

## 動作確認
生成後は必ず次を実行し、すべて通ることを確認してから提案する:

```bash
ruff check .
pytest --cov=cart --cov-report=term-missing
```
