```html
<!-- 无障碍数据表格 -->
<div role="table" aria-label="用户列表">
  <div role="rowgroup">
    <div role="row">
      <span role="columnheader" aria-sort="ascending">
        姓名
        <button aria-label="切换排序">▲</button>
      </span>
      <span role="columnheader">邮箱</span>
      <span role="columnheader">状态</span>
    </div>
  </div>
  <div role="rowgroup">
    <div role="row">
      <span role="cell">张三</span>
      <span role="cell">zhang@example.com</span>
      <span role="cell">活跃</span>
    </div>
  </div>
</div>

<!-- 路由切换焦点管理 -->
<script>
router.afterEach((to) => {
  // 通知屏幕阅读器页面已切换
  const announcer = document.getElementById("route-announcer");
  announcer.textContent = `已进入 ${to.meta.title}`;
  // 焦点移到内容区域顶部
  document.getElementById("main-content").focus();
});
</script>
```