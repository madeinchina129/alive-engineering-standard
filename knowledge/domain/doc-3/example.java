```java
// 订单聚合示例
public class Order {
    private OrderId id;           // 聚合根 ID
    private OrderStatus status;   // 状态
    private List<OrderLine> lines; // 内部实体
    private Address shippingAddress;
    private Money totalAmount;
    
    // 聚合根方法 - 保证不变量
    public void addItem(ProductId productId, int quantity, Money price) {
        // 检查订单状态（不可修改已支付的订单）
        if (status != OrderStatus.DRAFT) {
            throw new IllegalStateException("只能修改草稿状态的订单");
        }
        // 限制最大商品数量
        if (lines.size() >= 50) {
            throw new DomainException("单笔订单最多 50 件商品");
        }
        lines.add(new OrderLine(productId, quantity, price));
        recalculateTotal();
    }
    
    public void submit() {
        // 检查不变量
        if (lines.isEmpty()) {
            throw new DomainException("订单必须包含至少一件商品");
        }
        // 发布领域事件
        DomainEventPublisher.publish(new OrderSubmittedEvent(id));
    }
}
```