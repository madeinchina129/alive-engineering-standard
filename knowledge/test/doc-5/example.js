```javascript
// k6 负载测试脚本
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const apiTrend = new Trend('api_duration');

export const options = {
  stages: [
    { duration: '5m', target: 100 },   // 逐步增加到 100 并发
    { duration: '10m', target: 500 },  // 增加到 500 并发
    { duration: '5m', target: 1000 },  // 峰值 1000 并发
    { duration: '5m', target: 0 },     // 逐步减少
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    errors: ['rate<0.01'],             // 错误率 < 1%
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://staging.example.com';

export default function () {
  // 模拟用户搜索商品
  const searchResp = http.get(
    `${BASE_URL}/api/v1/products?q=耳机&page=1`,
    { tags: { name: 'search' } }
  );

  check(searchResp, {
    'search status is 200': (r) => r.status === 200,
    'search response < 500ms': (r) => r.timings.duration < 500,
  });

  apiTrend.add(searchResp.timings.duration);
  errorRate.add(searchResp.status !== 200);

  // 用户思考时间
  sleep(Math.random() * 3 + 1);  // 1-4 秒随机间隔
}

// 运行: k6 run --vus 10 --duration 30s load-test.js
```