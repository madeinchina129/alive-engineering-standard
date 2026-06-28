```java
// Spring Boot 集成测试示例
@SpringBootTest(classes = {OrderService.class, OrderRepository.class})
@Testcontainers
class OrderIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
            .withDatabaseName("testdb");

    @Container
    static GenericContainer<?> redis = new GenericContainer<>("redis:7")
            .withExposedPorts(6379);

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.redis.host", redis::getHost);
        registry.add("spring.redis.port", () -> redis.getMappedPort(6379));
    }

    @Autowired
    private OrderService orderService;

    @Autowired
    private OrderRepository orderRepository;

    @Test
    void testCreateAndRetrieveOrder() {
        // 创建订单
        Order order = orderService.createOrder(100L, List.of(
                new OrderItem(1L, "商品A", 2, new BigDecimal("99.99"))
        ));

        // 验证持久化
        Order saved = orderRepository.findById(order.getId());
        assertThat(saved).isNotNull();
        assertThat(saved.getStatus()).isEqualTo(OrderStatus.PENDING);
        assertThat(saved.getTotalAmount()).isEqualByComparingTo(new BigDecimal("199.98"));
    }

    @Test
    void testOrderStatusTransition() {
        Order order = orderService.createOrder(100L, testItems);

        orderService.payOrder(order.getId());
        assertThat(orderRepository.findById(order.getId()).getStatus())
                .isEqualTo(OrderStatus.PAID);

        orderService.shipOrder(order.getId());
        assertThat(orderRepository.findById(order.getId()).getStatus())
                .isEqualTo(OrderStatus.SHIPPED);
    }
}
```