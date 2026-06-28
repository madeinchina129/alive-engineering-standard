# RESTful API 设计规范 — FAQ

## Q1: PUT 和 PATCH 的区别？
PUT 是幂等的全量替换，PATCH 是非幂等的部分更新。例如更新用户信息：PUT 需要传全部字段（未传的字段重置为默认值），PATCH 只需传需要修改的字段。

## Q2: RESTful API 怎么处理批量操作？
使用自定义端点：POST /api/batch/users（批量创建），或者使用查询参数：DELETE /api/users?ids=1,2,3（批量删除）。不建议在标准资源端点上做批量操作。

## Q3: API 响应中应该包含多少数据？
默认响应包含核心字段（id、name、status 等）。如果客户端需要完整数据，使用查询参数 ?fields=all 或 ?include=detail,stats 按需加载。
