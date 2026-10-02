"""pricing モジュールのテスト（最小サンプル）。

これは「出発点」の最小テスト。
ここから Copilot に正常系・異常系・境界値を網羅させるのがデモの狙い。

テストの書き方の規約:
    - AAA パターン（Arrange / Act / Assert）
    - 複数入力は pytest.mark.parametrize を使う
    - 異常系は pytest.raises で例外を検証
"""

import pytest

from cart.pricing import Coupon, Item, calculate_subtotal, calculate_total


def test_calculate_subtotal_正常系():
    # Arrange: りんご100円×2 + みかん80円×3
    items = [
        Item(name="りんご", unit_price=100, quantity=2),
        Item(name="みかん", unit_price=80, quantity=3),
    ]

    # Act
    subtotal = calculate_subtotal(items)

    # Assert: 200 + 240 = 440
    assert subtotal == 440


def test_calculate_subtotal_空リストは例外():
    # Arrange
    items: list[Item] = []

    # Act & Assert
    with pytest.raises(ValueError):
        calculate_subtotal(items)


@pytest.mark.parametrize(
    ("coupon", "expected"),
    [
        (None, 1600),  # 小計1000 + 税100 + 送料500（5000円未満）
        (Coupon(kind="amount", value=200), 1380),  # 割引後800 + 税80 + 送料500
    ],
)
def test_calculate_total_クーポン有無(coupon, expected):
    # Arrange: 500円×2 = 小計1000円
    items = [Item(name="本", unit_price=500, quantity=2)]

    # Act
    total = calculate_total(items, coupon)

    # Assert
    assert total == expected
