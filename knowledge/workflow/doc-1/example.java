```java
// 状态机示例：订单状态机
public enum OrderState implements State {
    DRAFT, PENDING_PAYMENT, PAID, PROCESSING, SHIPPED, DELIVERED, COMPLETED, CANCELLED, REFUNDED;
}

public enum OrderEvent implements Event {
    SUBMIT, PAY, PROCESS, SHIP, DELIVER, COMPLETE, CANCEL, REFUND, TIMEOUT;
}

// 状态转换规则
public class OrderStateMachine {
    private StateMachine<OrderState, OrderEvent> machine;
    
    public OrderStateMachine() {
        machine = StateMachineBuilder.<OrderState, OrderEvent>builder()
            .initialState(OrderState.DRAFT)
            // 基本流程
            .transition(DRAFT, SUBMIT, PENDING_PAYMENT)
            .transition(PENDING_PAYMENT, PAY, PAID)
            .transition(PAID, PROCESS, PROCESSING)
            .transition(PROCESSING, SHIP, SHIPPED)
            .transition(SHIPPED, DELIVER, DELIVERED)
            .transition(DELIVERED, COMPLETE, COMPLETED)
            // 取消流程
            .transition(DRAFT, CANCEL, CANCELLED)
            .transition(PENDING_PAYMENT, CANCEL, CANCELLED)
            .transition(PAID, REFUND, REFUNDED)
            // 超时处理
            .transition(PENDING_PAYMENT, TIMEOUT, CANCELLED)
            // 前置校验
            .before(PAY, this::validatePayment)
            .after(PAY, this::notifyPaymentReceived)
            .build();
    }
}
```