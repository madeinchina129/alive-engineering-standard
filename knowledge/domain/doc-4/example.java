```java
// 领域事件定义示例
@Value
public class OrderSubmittedEvent implements DomainEvent {
    EventId eventId = EventId.generate();
    Instant occurredAt = Instant.now();
    OrderId orderId;
    UserId customerId;
    Money totalAmount;
    String eventType = "order.submitted";
    int version = 1;
}

// 事件发布（在聚合根方法中）
public class Order {
    public void submit() {
        validateForSubmission();
        this.status = OrderStatus.SUBMITTED;
        
        // 注册待发布事件（由基础设施在保存后自动发布）
        registerEvent(new OrderSubmittedEvent(this.id, this.customerId, this.totalAmount));
    }
}

// 事件消费（幂等处理）
@Component
public class InventoryEventHandler {
    @EventListener
    public void on(OrderSubmittedEvent event) {
        // 幂等校验
        if (processedEventRepository.exists(event.getEventId())) {
            log.info("Event already processed: {}", event.getEventId());
            return;
        }
        // 扣减库存
        inventoryService.reserveStock(event.getOrderId());
        // 记录已处理事件
        processedEventRepository.save(new ProcessedEvent(event.getEventId()));
    }
}
```