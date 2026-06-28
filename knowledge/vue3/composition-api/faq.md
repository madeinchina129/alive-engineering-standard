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
