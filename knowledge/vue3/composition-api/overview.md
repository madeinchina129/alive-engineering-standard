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
