# 端到端测试规范 — FAQ

## Q1: E2E 测试失败率很高怎么办？
首先区分「被测系统 Bug」和「测试 flakiness」。flakiness 通常由定时问题、异步等待不足、测试数据冲突导致。使用 Retry 机制（重试 2-3 次）和重试间隔解决。

## Q2: Playwright vs Cypress vs Selenium？
Playwright（推荐）：跨浏览器、速度快、API 现代化、支持移动端。Cypress：调试体验好、社区大、但只支持 Chrome。Selenium：老牌工具、生态丰富、但速度慢。
