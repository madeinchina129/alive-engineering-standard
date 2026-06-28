# Composition API 使用规范

## 组件书写规范

### 使用 `<script setup>` 语法

```vue
<!-- ✅ 推荐：<script setup> -->
<script setup lang="ts">
import { ref, computed } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)
</script>

<!-- ❌ 避免：setup() 函数 -->
<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
export default defineComponent({
  setup() {
    const count = ref(0)
    const doubled = computed(() => count.value * 2)
    return { count, doubled }
  }
})
</script>
```

### 逻辑按功能分组

```vue
<script setup lang="ts">
// 1. Props 和 Emits
const props = defineProps<{ userId: string }>();
const emit = defineEmits<{ update: [data: User] }>();

// 2. Composables
const { user, isLoading, error } = useUser(props.userId);

// 3. 本地响应式状态
const isEditing = ref(false);
const form = ref<UserForm>({ name: '', email: '' });

// 4. 计算属性
const canSubmit = computed(() => form.value.name.length > 0);

// 5. 生命周期
watch(user, (newUser) => { form.value = toUserForm(newUser); });
onMounted(() => { /* ... */ });

// 6. 方法
async function handleSubmit() { /* ... */ }
</script>
```

## 强制规则 (MUST)

### 1. 使用 ref 和 computed 替代 data

```typescript
// ✅ 正确
const count = ref(0);
const doubled = computed(() => count.value * 2);

// ❌ 避免
const state = reactive({ count: 0, doubled: 0 });
watch(() => state.count, (v) => { state.doubled = v * 2; });
```

### 2. 导出 composable 函数命名使用 useXxx

```typescript
// ✅ 正确
export function useUser(id: string) { /* ... */ }
export function usePermission() { /* ... */ }

// ❌ 错误
export function fetchUser(id: string) { /* 这是函数，不是 composable */ }
```

### 3. composable 返回值应解构后使用

```typescript
// ✅ 正确：解构 ref
const { user, isLoading } = useUser(props.id);

// ✅ 正确：如果不想解构，保留对象
const userState = useUser(props.id);
// userState.user.value / userState.isLoading.value

// ❌ 错误：解构 reactive 会丢失响应性
const { user, isLoading } = toRefs(useUser(props.id)); // 除非 composable 内部使用 reactive
```

### 4. watch 和 watchEffect 需清理副作用

```typescript
// ✅ 正确：watch 返回取消函数
const stop = watch(source, callback);

// 组件卸载时自动停止
onUnmounted(() => stop());

// ✅ 正确：watchEffect 自动追踪
watchEffect(async () => {
  const response = await fetch(`/api/users/${userId.value}`);
  user.value = await response.json();
});
```

### 5. 避免在模板中使用复杂表达式

```vue
<!-- ✅ 推荐：计算属性 -->
<script setup>
const fullName = computed(() => `${user.value.lastName} ${user.value.firstName}`);
</script>
<template>
  <div>{{ fullName }}</div>
</template>

<!-- ❌ 避免：模板中的表达式 -->
<template>
  <div>{{ `${user.lastName} ${user.firstName}`.trim() }}</div>
</template>
```

## 推荐实践 (SHOULD)

### 1. 提取复杂逻辑到 composable

```typescript
// ✅ 推荐：提取分页逻辑
const { page, pageSize, total, data, loadPage } = usePagination(fetchUsers);
```

### 2. 使用 defineProps 和 defineEmits 的类型注解

```vue
<script setup lang="ts">
const props = defineProps<{
  title: string;
  items: Item[];
  visible?: boolean;
}>();
</script>
```

### 3. defineExpose 明确暴露的内容

```vue
<script setup lang="ts">
const internalMethod = () => { /* ... */ };
defineExpose({ internalMethod });
</script>
```

## 禁止行为 (MUST NOT)

- ❌ 在 setup 中使用 `this`
- ❌ 在 `<script setup>` 中使用 `export default`
- ❌ 在 composable 外部使用 reactive/ref
- ❌ 在 watch 回调中修改被 watch 的值（可能导致循环）
- ❌ 在异步回调中访问已卸载组件的响应式状态（可能内存泄漏）
