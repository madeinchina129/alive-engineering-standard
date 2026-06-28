```html
<!-- ✅ 无障碍友好的表单 -->
<div class="form-field">
  <label for="email">电子邮箱</label>
  <input
    id="email"
    type="email"
    aria-describedby="email-help email-error"
    aria-invalid="false"
    required
  />
  <p id="email-help" class="help-text">请输入工作邮箱</p>
  <p id="email-error" class="error-text" role="alert"></p>
</div>

<!-- ❌ 无障碍不友好的表单 -->
<div class="form-field">
  <span>邮箱</span>
  <input type="email" placeholder="输入邮箱" />
</div>
```