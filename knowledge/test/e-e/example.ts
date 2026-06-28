```typescript
import { test, expect } from '@playwright/test';

test.describe('电商下单流程', () => {

  test.beforeEach(async ({ page }) => {
    // 使用 data-testid 等待元素
    await page.goto('/');
    await page.waitForSelector('[data-testid="home-page"]');
  });

  test('完整购物流程: 搜索→加购→下单→支付', async ({ page }) => {
    // 1. 搜索商品
    await page.fill('[data-testid="search-input"]', '无线耳机');
    await page.click('[data-testid="search-button"]');
    await expect(page.locator('[data-testid="product-list"]')).toBeVisible();

    // 2. 选择商品加入购物车
    await page.click('[data-testid="product-card"]:first-child [data-testid="add-to-cart"]');
    await expect(page.locator('[data-testid="cart-count"]')).toHaveText('1');

    // 3. 进入购物车
    await page.click('[data-testid="cart-icon"]');
    await expect(page.locator('[data-testid="cart-page"]')).toBeVisible();
    await page.click('[data-testid="checkout-button"]');

    // 4. 填写收货地址并下单
    await page.fill('[data-testid="address-input"]', '北京市朝阳区...');
    await page.click('[data-testid="submit-order"]');

    // 5. 支付
    await page.click('[data-testid="pay-button"]');
    await expect(page.locator('[data-testid="order-success"]')).toBeVisible();
    await expect(page.locator('[data-testid="order-status"]')).toHaveText('支付成功');
  });

  test('搜索无结果时显示空状态', async ({ page }) => {
    await page.fill('[data-testid="search-input"]', '!@#$%^&*()');
    await page.click('[data-testid="search-button"]');
    await expect(page.locator('[data-testid="empty-state"]')).toBeVisible();
    await expect(page.locator('[data-testid="empty-state-message"]'))
      .toContainText('未找到相关商品');
  });
});
```