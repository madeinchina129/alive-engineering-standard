```java
// Saga 编排示例：下单流程
@Component
public class CreateOrderSaga implements Saga<CreateOrderRequest> {
    
    @Override
    public void define(SagaDefinition<CreateOrderRequest> saga) {
        saga.step("reserveInventory")
            .invoke(inventoryService::reserve)  // 正向操作
            .withCompensation(inventoryService::release)  // 补偿操作
            .onReply(InventoryReserved.class, this::onInventoryReserved)
            .onError(this::onInventoryError);
        
        saga.step("processPayment")
            .invoke(paymentService::charge)
            .withCompensation(paymentService::refund)
            .onReply(PaymentProcessed.class, this::onPaymentProcessed);
        
        saga.step("prepareShipping")
            .invoke(shippingService::prepare)
            .withCompensation(shippingService::cancel)
            .onReply(ShippingPrepared.class, this::onShippingPrepared);
    }
    
    @SagaEventHandler(associativeWith = "reserveInventory")
    public void onInventoryReserved(InventoryReserved event, SagaState state) {
        log.info("库存预留成功");
    }
    
    public void onInventoryError(Throwable error, SagaState state) {
        log.error("库存预留失败，开始补偿流程");
        // Saga 框架自动执行已通过步骤的补偿操作
    }
}
```