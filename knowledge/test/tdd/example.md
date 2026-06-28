```python
# TDD 三步循环示例: 计算购物车总价

# Step 1: RED - 先写测试
import pytest

def test_calculate_cart_total_with_multiple_items():
    cart = [
        {'price': 10.0, 'qty': 2},  # 20
        {'price': 15.5, 'qty': 1},  # 15.5
        {'price': 5.0, 'qty': 3},   # 15
    ]
    assert calculate_total(cart) == 50.5

def test_calculate_cart_total_with_empty_cart():
    assert calculate_total([]) == 0.0

def test_calculate_cart_total_applies_discount():
    cart = [{'price': 100, 'qty': 1}]
    assert calculate_total(cart, discount=0.1) == 90.0

# Step 2: GREEN - 最简实现（让测试通过）
def calculate_total(cart, discount=0):
    total = sum(item['price'] * item['qty'] for item in cart)
    return total * (1 - discount)

# Step 3: REFACTOR - 重构（不改变行为）
from dataclasses import dataclass

@dataclass
class CartItem:
    price: float
    quantity: int

def calculate_total(items: list[CartItem], discount: float = 0) -> float:
    """计算购物车总价，支持折扣"""
    subtotal = sum(item.price * item.quantity for item in items)
    return round(subtotal * (1 - discount), 2)

# 再次运行测试确认全部通过 ✅
```

# 持续集成提示
# 在 CI 中运行测试并检查覆盖率
# git commit 前运行所有测试（使用 pre-commit hook）