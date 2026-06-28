```python
import pytest
from unittest.mock import Mock, patch
from src.order_service import OrderService

# Builder 模式构建测试数据
class OrderBuilder:
    def __init__(self):
        self.id = 1
        self.user_id = 100
        self.total_amount = 99.99
        self.status = 'pending'

    def with_status(self, status):
        self.status = status
        return self

    def build(self):
        return Order(id=self.id, user_id=self.user_id,
                     total_amount=self.total_amount, status=self.status)

# 测试类
class TestOrderService:

    def test_create_order_success_when_valid_input(self):
        """验证有效输入时成功创建订单"""
        # Arrange
        mock_repo = Mock()
        mock_repo.save.return_value = OrderBuilder().build()
        service = OrderService(repo=mock_repo, payment=Mock())

        # Act
        result = service.create_order(user_id=100, items=[{'id': 1, 'qty': 2}])

        # Assert
        assert result.id == 1
        assert result.status == 'pending'
        mock_repo.save.assert_called_once()

    def test_create_order_fails_when_user_not_found(self):
        """验证用户不存在时创建失败"""
        # Arrange
        mock_user = Mock()
        mock_user.get_by_id.return_value = None
        service = OrderService(user_service=mock_user, repo=Mock())

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            service.create_order(user_id=999, items=[{'id': 1, 'qty': 2}])

    @pytest.mark.parametrize("items,expected", [
        ([{'id': 1, 'qty': 0}], 0),
        ([{'id': 1, 'qty': -1}], 0),
        ([], 0),
    ])
    def test_calculate_total_with_edge_case_quantities(self, items, expected):
        """验证边界数量值的计算"""
        service = OrderService(repo=Mock())
        assert service.calculate_total(items) == expected
```