"""ショッピングカートの価格計算ロジック。

Copilotによる自動テスト生成のデモ題材。
正常系・異常系・境界値のテストが書きやすいように、
純粋関数として分岐を持たせている。
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    """カートに入れる商品1行。

    Attributes:
        name: 商品名。
        unit_price: 単価（円、0以上の整数を想定）。
        quantity: 数量（1以上の整数を想定）。
    """

    name: str
    unit_price: int
    quantity: int


@dataclass(frozen=True)
class Coupon:
    """割引クーポン。

    kind が "rate" なら value は割引率(0〜1)、
    "amount" なら value は割引額(円)。
    """

    kind: str  # "rate" または "amount"
    value: float


def calculate_subtotal(items: list[Item]) -> int:
    """商品リストの小計（税抜）を計算する。

    Args:
        items: 商品のリスト。空リストは不可。

    Returns:
        小計金額（円）。

    Raises:
        ValueError: items が空、または単価/数量が不正な場合。
    """
    if not items:
        raise ValueError("商品が1つもありません")

    subtotal = 0
    for item in items:
        if item.unit_price < 0:
            raise ValueError(f"単価が負の値です: {item.name}")
        if item.quantity < 1:
            raise ValueError(f"数量は1以上にしてください: {item.name}")
        subtotal += item.unit_price * item.quantity
    return subtotal


def apply_discount(subtotal: int, coupon: Coupon | None) -> int:
    """小計にクーポン割引を適用する。

    Args:
        subtotal: 割引前の小計（0以上）。
        coupon: 適用するクーポン。None の場合は割引なし。

    Returns:
        割引後の金額（0未満にはならない）。

    Raises:
        ValueError: クーポン種別が不正、または割引率が範囲外の場合。
    """
    if subtotal < 0:
        raise ValueError("小計が負の値です")
    if coupon is None:
        return subtotal

    if coupon.kind == "rate":
        if not 0 <= coupon.value <= 1:
            raise ValueError("割引率は0〜1の範囲で指定してください")
        discounted = subtotal * (1 - coupon.value)
        return int(math.floor(discounted))

    if coupon.kind == "amount":
        return max(0, subtotal - int(coupon.value))

    raise ValueError(f"不明なクーポン種別です: {coupon.kind}")


def calculate_tax(amount: int, rate: float = 0.10) -> int:
    """消費税額を計算する（端数は切り捨て）。

    Args:
        amount: 税抜金額（0以上）。
        rate: 税率（デフォルト10%）。

    Returns:
        消費税額（円、切り捨て）。

    Raises:
        ValueError: amount が負、または rate が負の場合。
    """
    if amount < 0:
        raise ValueError("金額が負の値です")
    if rate < 0:
        raise ValueError("税率が負の値です")
    return int(math.floor(amount * rate))


def shipping_fee(subtotal: int, free_threshold: int = 5000, fee: int = 500) -> int:
    """送料を計算する。一定額以上で送料無料。

    Args:
        subtotal: 税抜小計。
        free_threshold: この金額以上で送料無料になる閾値。
        fee: 閾値未満のときの送料。

    Returns:
        送料（円）。
    """
    if subtotal >= free_threshold:
        return 0
    return fee


def calculate_total(items: list[Item], coupon: Coupon | None = None) -> int:
    """合計金額（割引・税・送料込み）を計算する。

    計算順序:
        1. 小計を計算
        2. クーポン割引を適用
        3. 割引後の金額に消費税を加算
        4. （割引前の）小計を基準に送料を加算

    Args:
        items: 商品リスト。
        coupon: 適用するクーポン（任意）。

    Returns:
        支払総額（円）。
    """
    subtotal = calculate_subtotal(items)
    discounted = apply_discount(subtotal, coupon)
    tax = calculate_tax(discounted)
    shipping = shipping_fee(subtotal)
    return discounted + tax + shipping
