# 手順①：手元の Copilot でテストを生成する

VS Code の **GitHub Copilot Chat** を使って、`src/cart/pricing.py` のテストを
自動生成する手順です。発表デモのステップ2に対応します。

## 事前準備

- VS Code に **GitHub Copilot** と **GitHub Copilot Chat** 拡張機能を入れ、サインイン済みにする。
- `python -m pip install -e ".[dev]"` を実行済み（pytest / ruff が使える状態）。
- `.github/copilot-instructions.md` がリポジトリにある（Copilot が規約を自動参照する）。

## やり方A：スラッシュコマンド `/tests`（お手軽）

1. `src/cart/pricing.py` をエディタで開く。
2. テストを作りたい関数（例：`calculate_total`）を選択する。
3. Copilot Chat を開き、次を入力:

   ```
   /tests 選択した関数の pytest テストを作って。
   正常系・異常系・境界値を parametrize で網羅して。
   ```

4. 生成されたテストを `tests/test_pricing.py` に貼り付ける。
5. `pytest -v` を実行して通ることを確認。失敗したら次項のプロンプトで修正を依頼。

## やり方B：プロンプトで細かく指示（網羅性重視）

Copilot Chat に、ファイルを `#` で参照しつつ依頼します。

### プロンプト例1：関数ごとに網羅

```
#file:src/cart/pricing.py の apply_discount のテストを pytest で書いて。
- rate クーポン（0%, 50%, 100%）、amount クーポン、None の各ケース
- 割引率が範囲外(-0.1, 1.1)のとき ValueError になること
- 小計が負のとき ValueError になること
AAAパターンで、@pytest.mark.parametrize を使ってまとめて。
```

### プロンプト例2：境界値を狙い撃ち

```
#file:src/cart/pricing.py の shipping_fee について、
送料無料になる境界値（free_threshold ちょうど / 1円下 / 1円上）を
検証する pytest テストを parametrize で書いて。
```

### プロンプト例3：端数処理の検証

```
#file:src/cart/pricing.py の calculate_tax は端数を切り捨てる仕様。
amount=109（税10%→10.9）のとき 10 になることなど、
切り捨てが効くケースを含めてテストして。
```

## 生成後に必ずやること

```bash
ruff check .                                   # Lint を通す
pytest --cov=cart --cov-report=term-missing    # テスト＋カバレッジ確認
```

- 赤くなったテストは「仕様 vs 実装」どちらが正しいかを確認。
  Copilot の期待値が間違っていることもあるので、鵜呑みにしない。
- カバレッジの `Missing` 行を見て、未カバーの分岐を追加依頼する:

  ```
  pricing.py のうちテストが通っていない分岐（例: 数量が0のとき）を
  カバーするテストを追加して。
  ```

## デモの見せ場

- **Before**: `tests/test_pricing.py` は3ケースだけ。カバレッジも低い。
- **After**: Copilot で一気に網羅し、カバレッジが上がる様子をターミナルで見せる。

> 次は手順②（`02_copilot_coding_agent.md`）で、この生成を
> **GitHub 上で自動化**する方法に進みます。
