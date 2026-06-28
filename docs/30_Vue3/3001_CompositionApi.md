---
id: vue3.composition_api
priority: P0
owner: Frontend Team
version: 1.0
generated: 2026-06-28
---

# Composition API 规范

> **领域**: Vue3 开发规范 | **优先级**: P0 | **版本**: 1.0
> 
> Vue3 Composition API 使用标准，setup/ref/reactive/computed 规范



---

---

# Composition API 使用方案

## 为什么选择 Composition API

### 更好的逻辑复用

```vue
<script setup lang="ts">
// ✅ 逻辑可以提取到 composable 中复用
const { user, isLoading, error } = useUser(route.params.id);
const { formatDate } = useDateFormat();
</script>
```

对比 Options API 的 mixin 存在命名冲突和来源不明的问题。

### 类型推断

```typescript
// ✅ TypeScript 完美推断
const count = ref(0); // Ref<number>
const user = ref<User | null>(null); // Ref<User | null>

const doubled = computed(() => count.value * 2); // ComputedRef<number>
```

### 按功能组织，而非按选项类型

```vue
<script setup lang="ts">
// ✅ 相关逻辑组织在一起
// --- 用户认证 ---
const token = useToken();
const { login, logout, isAuthenticated } = useAuth();

// --- 用户数据 ---
const { user, updateUser } = useUser();

// --- UI 状态 ---
const { theme, toggleTheme } = useTheme();
</script>
```

对比 Options API 将同一功能的 data/methods/watch 分散在不同区块。

---

## 对比 Options API

| 维度 | Options API | Composition API |
|------|------------|----------------|
| 逻辑复用 | mixin（冲突风险） | composable（完美） |
| 类型推断 | 有限 | 完整 |
| 代码组织 | 按选项类型 | 按功能逻辑 |
| 学习曲线 | 低 | 中 |
| Tree-shaking | 不支持 | 支持 |
| 大型组件 | 难以维护 | 易于拆分 |

---

## 适用范围

- **强制使用**：所有新 Vue3 项目使用 Composition API
- **推荐**：`<script setup>` 语法
- **兼容**：Options API 组件可以通过 `mixins: [compositionMixin]` 逐步迁移

## 与项目其他部分的集成

- **Pinia**：Store 中使用 Composition API 定义状态和操作
- **Vue Router**：`useRoute()` / `useRouter()` composables
- **Element Plus**：通过 composable 封装对话框/表格逻辑


---

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
  <div></div>
</template>

<!-- ❌ 避免：模板中的表达式 -->
<template>
  <div></div>
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


---

# Composition API FAQ

## Q: ref 和 reactive 如何选择？

A:
```typescript
// ✅ 简单值 → ref
const count = ref(0);
const name = ref('');

// ✅ 对象但需要替换整个值 → ref
const user = ref<User | null>(null);
user.value = newUser; // 可以重新赋值

// ✅ 普通对象 → reactive
const form = reactive({ name: '', email: '' });

// ⚠️ reactive 不能重新赋值
// ❌ form = reactive({ ... })  // 这不会工作
```

推荐默认使用 ref，需要对象响应式且不需要重新赋值时使用 reactive。

## Q: `<script setup>` 和 `setup()` 函数怎么选？

A: 新项目一律使用 `<script setup>`。优势：
- 更少的样板代码（不需要 return）
- 更好的 TypeScript 支持
- 可以直接使用 await

## Q: 在 composable 中如何提供响应式数据？

```typescript
// ✅ 推荐：返回 ref/computed
export function useCounter(initial = 0) {
  const count = ref(initial);
  const doubled = computed(() => count.value * 2);
  const increment = () => count.value++;
  return { count, doubled, increment };
}

// ✅ 或者使用 toRefs 包裹 reactive
export function useMouse() {
  const state = reactive({ x: 0, y: 0 });
  // ...
  return toRefs(state);
}
```

## Q: watch 和 watchEffect 的区别？

- **watch**：需要指定监听源，可以获取新旧值，懒执行
- **watchEffect**：自动追踪依赖，立即执行，不能获取旧值

```typescript
// watch: 明确知道要监听什么
watch(searchQuery, async (newQuery, oldQuery) => {
  if (newQuery !== oldQuery) {
    results.value = await search(newQuery);
  }
});

// watchEffect: 不知道具体依赖什么
watchEffect(async () => {
  results.value = await search(searchQuery.value, page.value);
});
```

## Q: 如何处理组件卸载后的异步回调？

```typescript
// ✅ 使用 aborted flag 或 onUnmounted
onUnmounted(() => { isCancelled = true; });

async function fetchData() {
  const response = await api.get('/data');
  if (!isCancelled) {
    data.value = response;
  }
}
```

## Q: defineProps 的泛型语法和运行时声明怎么选？

```typescript
// ✅ 纯类型（推荐，没有运行时校验）
const props = defineProps<{ title: string; count?: number }>();

// ✅ 运行时（需要校验时）
const props = defineProps({
  title: { type: String, required: true },
  count: { type: Number, default: 0 },
});
```


---

# Composition API Code Review Checklist

## 组件结构
- [ ] 是否使用 `<script setup>` 语法？
- [ ] 逻辑是否按功能分组组织？
- [ ] 是否避免在 setup 中使用 `this`？
- [ ] 是否使用了 `defineProps`/`defineEmits` 类型注解？

## 响应式
- [ ] 简单类型是否使用 ref？
- [ ] 对象需要重新赋值时是否使用 ref 而非 reactive？
- [ ] computed 是否用于派生状态？
- [ ] 是否避免了在模板中使用复杂表达式？

## Composable
- [ ] composable 函数是否以 `use` 开头命名？
- [ ] composable 是否返回可使用解构的值？
- [ ] composable 是否处理了组件卸载后的清理？
- [ ] 是否提取了可复用的复杂逻辑？

## 副作用管理
- [ ] watch 是否指定了精确的监听源？
- [ ] 异步操作是否有组件卸载保护？
- [ ] watchEffect 是否追踪了正确的依赖？
- [ ] 定时器/事件监听是否在 onUnmounted 中清理？

## 类型安全
- [ ] 组件 Props 是否有类型定义？
- [ ] ref 是否显式标注了类型？（ref<T>）
- [ ] emit 事件是否有类型定义？
- [ ] 是否避免使用 any 类型？

## 性能
- [ ] 是否避免了不必要 watcher？
- [ ] 是否使用了 shallowRef 处理大型对象？
- [ ] 组件拆分是否合理？（避免过大组件）


---

你是一个 Vue3 前端专家，精通 Composition API。请根据以下规范回答问题。

## 核心规范

### 组件书写
- 使用 `<script setup lang="ts">` 语法
- 逻辑按功能分组：Props/Emits → Composables → 本地状态 → 计算属性 → 生命周期 → 方法
- 禁止在 setup 中使用 `this`
- 使用 `defineProps<T>()` 和 `defineEmits<T>()` 类型注解

### 响应式
- 简单类型 / 需要替换的值 → ref
- 纯对象（无需替换） → reactive
- 派生状态 → computed
- 复杂表达式转移到 computed 或函数

### Composable
- 命名格式：`useXxx`
- 返回值支持解构使用
- 处理组件卸载后的清理

### 副作用管理
- watch 指定精确监听源
- watchEffect 自动追踪
- 异步操作有卸载保护
- 定时器/事件在 onUnmounted 清理

### 类型安全
- 避免 any
- Props/Emits 有类型定义
- ref<T> 显式类型

## 代码审查检查
审查时检查：script setup 使用、逻辑分组、ref/reactive 选择、composable 命名、watch 清理、类型注解。



---

*本文档由 AES Knowledge Generator 自动生成。知识源：`knowledge/vue3/composition-api/`*
