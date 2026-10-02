# cart-demo — Copilot自動テスト作成 + GitHub PR CI デモ

技術発表会用のサンプルプロジェクトです。
**「GitHub Copilot にテストを書かせ、Pull Request を作ると CI が自動で回る」** 一連の流れを体験できます。

## 構成

```
.
├── .github/
│   ├── workflows/ci.yml          # PR/push で動く CI（ruff Lint + pytest + カバレッジ）
│   └── copilot-instructions.md   # Copilot への共通ルール（手元/agent 両方が参照）
├── src/cart/pricing.py           # サンプルロジック（小計・割引・税・送料・合計）
├── tests/test_pricing.py         # pytest の最小サンプル（ここから Copilot で網羅）
├── pyproject.toml                # 依存・pytest・ruff・coverage 設定
└── docs/
    ├── 01_copilot_local_test_gen.md   # 手元 Copilot でのテスト生成手順
    └── 02_copilot_coding_agent.md     # GitHub Copilot coding agent での PR 自動生成手順
```

## セットアップ

```bash
# 仮想環境を作成して有効化（Windows / Git Bash）
python -m venv .venv
source .venv/Scripts/activate      # PowerShell: .venv\Scripts\Activate.ps1

# 開発用依存をインストール
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## ローカルでの実行

```bash
# テスト（カバレッジ付き）
pytest --cov=cart --cov-report=term-missing

# Lint
ruff check .
```

## 発表デモの流れ（5ステップ）

1. **ロジックを見せる** — `src/cart/pricing.py` の関数（分岐あり）を紹介。
2. **Copilot にテストを書かせる** — `docs/01_copilot_local_test_gen.md` の手順で
   正常系・異常系・境界値のテストを生成（手元の VS Code Copilot Chat）。
3. **PR を作る** — ブランチを切ってテストを追加し、GitHub へ push → Pull Request 作成。
4. **CI が自動で回る** — PR 上で `ruff` と `pytest` が走り、結果が緑になる様子を見せる。
5. **（応用）Copilot coding agent** — `docs/02_copilot_coding_agent.md` の手順で、
   GitHub 上の Issue を Copilot にアサイン → テスト追加 PR が**自動生成**される様子を見せる。

## CI について

`.github/workflows/ci.yml` が `main` 向けの **Pull Request** と **push** で発火します。
Python 3.10 / 3.12 のマトリクスで、Lint → テスト → カバレッジ出力を実行します。

> GitHub へのリモート作成・push・ブランチ保護の設定手順は
> `docs/02_copilot_coding_agent.md` にまとめています。
