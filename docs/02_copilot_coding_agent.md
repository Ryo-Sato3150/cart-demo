# 手順②：GitHub で CI を構築し、Copilot coding agent に PR を自動生成させる

ローカルのプロジェクトを GitHub に載せ、**Pull Request で CI が自動で回る**状態にし、
さらに **Copilot coding agent** に Issue を割り当ててテスト追加 PR を自動生成させる手順です。
発表デモのステップ3〜5に対応します。

---

## パート1：GitHub にリポジトリを作って push する

### 1-1. ローカルを Git リポジトリにする

```bash
cd "c:/技術発表会お試し"
git init
git add -A
git commit -m "init: cart-demo（Copilotテスト生成 + CI）"
git branch -M main
```

### 1-2. GitHub 側にリポジトリを作る

**方法A：ブラウザ（gh CLI なしでOK）**

1. <https://github.com/new> を開く。
2. Repository name に `cart-demo` 等を入力。README 等は**追加しない**（空で作る）。
3. 「Create repository」を押す。
4. 表示される「…or push an existing repository」のコマンドをコピーして実行:

   ```bash
   git remote add origin https://github.com/<ユーザー名>/cart-demo.git
   git push -u origin main
   ```

**方法B：gh CLI（導入済みなら一発）**

```bash
# 未導入なら: winget install --id GitHub.cli  → 新しいシェルで gh auth login
gh auth login
gh repo create cart-demo --private --source=. --remote=origin --push
```

### 1-3. CI が動くことを確認

- push 後、GitHub の **Actions** タブに「CI」ワークフローが現れる。
- `.github/workflows/ci.yml` が `main` への push で発火し、Lint→テスト→カバレッジが走る。

---

## パート2：Pull Request で CI を回すデモ

1. ブランチを切る:

   ```bash
   git switch -c add-tests
   ```

2. 手順①（`01_copilot_local_test_gen.md`）で生成したテストを `tests/` に追加・コミット。

   ```bash
   git add -A
   git commit -m "test: pricing の正常系/異常系/境界値を追加"
   git push -u origin add-tests
   ```

3. GitHub 上で **Pull Request** を作成（base: `main` ← compare: `add-tests`）。
4. PR の「Checks」で **CI が自動実行**される様子を見せる。
   - 緑（成功）になったら「Merge」できる、というのがデモの締め。

### （任意）緑でないとマージできないようにする = ブランチ保護

発表で「CI が通らないとマージできない」を見せたい場合:

1. リポジトリの **Settings → Branches → Add branch ruleset**（または Branch protection rules）。
2. 対象ブランチを `main` に指定。
3. **Require status checks to pass before merging** を ON。
4. 必須チェックに CI のジョブ（例: `Lint & Test (Python 3.12)`）を追加。
   - ※ジョブ名は一度 CI を実行した後でないと候補に出ないことがある。

---

## パート3：Copilot coding agent にテスト PR を自動生成させる

> **前提**：Copilot coding agent は **GitHub Copilot の対象プラン**（Pro/Pro+ または
> Business/Enterprise で管理者が有効化）で使えます。組織リポジトリの場合は管理者設定が必要です。
> 利用可否・UIは変わることがあるため、最新は GitHub のドキュメントを確認してください。

### 3-1. 有効化を確認

- 個人：<https://github.com/settings/copilot> で Copilot が有効か確認。
- 組織：Organization の **Settings → Copilot → Policies** で coding agent を許可。

### 3-2. Issue を作って Copilot に割り当てる

1. リポジトリの **Issues → New issue** でタスクを書く。テスト生成を依頼する例:

   **タイトル**
   ```
   pricing.py のテストカバレッジを上げる
   ```

   **本文**
   ```
   src/cart/pricing.py の全関数について pytest のテストを追加してください。

   要件:
   - 正常系・異常系(ValueError)・境界値を網羅する
   - @pytest.mark.parametrize でまとめる
   - calculate_tax の端数切り捨て、shipping_fee の送料無料境界を必ず検証
   - ruff check . と pytest が通ること

   規約は .github/copilot-instructions.md に従ってください。
   ```

2. Issue 右側の **Assignees** で **Copilot** を選択（または `#github-pull-request_copilot-coding-agent` 等、UI上の該当エントリ）。
3. しばらくすると Copilot が作業し、**ドラフト PR** が自動で作成される。
   - PR 上では Copilot が変更内容・テスト結果を説明してくれる。

### 3-3. 自動生成された PR をレビュー

- PR の **Checks** で、前述の CI（ruff + pytest）が自動で回る。
- 変更差分を確認し、問題なければコメントで追加依頼も可能:

  ```
  @copilot calculate_subtotal の「数量が0」のケースも追加して
  ```

- 緑になったらレビュー承認 → マージ。

---

## デモ全体のストーリー（まとめ）

| ステップ | 何を見せる | 使うもの |
|---|---|---|
| 1 | 分岐のあるロジック | `src/cart/pricing.py` |
| 2 | 手元でテスト自動生成 | VS Code Copilot Chat（手順①） |
| 3 | PR 作成 | `git push` + GitHub PR |
| 4 | PR で CI 自動実行 | `.github/workflows/ci.yml` |
| 5 | Issue から PR 自動生成 | GitHub Copilot coding agent |

> 迷ったら README の「発表デモの流れ（5ステップ）」も参照。
