```python
# 事件溯源示例：订单聚合
from dataclasses import dataclass
from enum import Enum

class OrderStatus(Enum):
    DRAFT = 'draft'
    SUBMITTED = 'submitted'
    PAID = 'paid'
    SHIPPED = 'shipped'

@dataclass
class OrderState:
    order_id: str
    status: OrderStatus
    items: list
    total_amount: float
    version: int
    
class OrderAggregate:
    def __init__(self):
        self.state = None
        self.changes = []
    
    def load_from_history(self, events):
        self.state = None
        for event in events:
            self._apply(event)
    
    def submit(self, order_id, items):
        event = OrderSubmitted(order_id, items, sum(i['price']*i['qty'] for i in items))
        self._apply(event)
        self.changes.append(event)
    
    def pay(self, payment_id):
        event = OrderPaid(self.state.order_id, payment_id)
        self._apply(event)
        self.changes.append(event)
    
    def _apply(self, event):
        if isinstance(event, OrderSubmitted):
            self.state = OrderState(
                order_id=event.order_id,
                status=OrderStatus.SUBMITTED,
                items=event.items,
                total_amount=event.total,
                version=1
            )
        elif isinstance(event, OrderPaid):
            self.state.status = OrderStatus.PAID
            self.state.version += 1
```