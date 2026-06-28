# RESTful API 规范 — FAQ

## Q1: 如何设计分页？
使用 ?page=1&size=20 参数，响应包含 total/pages/items。

## Q2: 如何表示关联资源？
使用嵌套路由：/api/users/{id}/orders。
