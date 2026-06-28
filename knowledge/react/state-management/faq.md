# React 状态管理 FAQ

## Q: Zustand 和 Context 怎么选？

```
Zustand：全局状态，selector 细粒度订阅，无 Provider 嵌套
Context：主题/语言/认证等低频更新，需要 Provider
```

```tsx
// Zustand：任意组件直接使用
const useStore = create(set => ({ bears: 0, increase: () => set(s => ({ bears: s.bears + 1 })) }))

// Context：需要 Provider 包裹消费组件
const ThemeContext = createContext('light')
<ThemeContext.Provider value="dark"><App /></ThemeContext.Provider>
```

## Q: 为什么表单状态不该放全局 store？

每次按键触发全局 store 更新，所有 selector 重新计算，导致不必要的渲染。表单状态应该局限在组件内。

## Q: TanStack Query 和 Zustand 重复怎么办？

```
TanStack Query：服务端缓存层，管理 API 数据
Zustand：客户端全局状态，管理 UI 状态（侧边栏开关、主题等）
```

两者不冲突，分别管理不同层面的状态。

## Q: `useStore(s => s.user?.name)` 为什么不会全量重渲染？

Zustand 使用 === 比较 selector 返回值。如果 `s.user?.name` 不变，组件不重渲染。这就是为什么需要细粒度 selector。

## Q: 什么时候需要 Redux Toolkit？

```
- 超大型应用（50+ 页面）
- 复杂的状态交互
- 团队多人协作需要强约束
- 已有 Redux 基础设施
```

对于中小项目，Zustand 就够了。
