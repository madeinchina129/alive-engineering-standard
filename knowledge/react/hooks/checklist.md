# React Hooks Code Review Checklist

## 规则遵守
- [ ] Hooks 是否在顶层调用？
- [ ] 是否不在条件/循环/嵌套函数中调用 Hooks？
- [ ] 自定义 Hook 是否以 `use` 开头？
- [ ] 是否不在非组件/非 Hook 中使用 Hooks？

## useState
- [ ] 是否避免了不必要的 state？（可从 props 计算的值）
- [ ] 复杂初始化是否使用了惰性初始化？
- [ ] 状态更新是否使用函数式更新？（当新值依赖旧值时）

## useEffect
- [ ] 依赖数组是否完整？
- [ ] 是否避免了 useEffect 直接 async？
- [ ] 订阅/定时器是否有清理函数？
- [ ] 是否避免了不必要的 useEffect？（派生值用 useMemo）
- [ ] 网络请求是否有取消机制？（AbortController）

## useMemo / useCallback
- [ ] 是否只用于计算昂贵的操作？
- [ ] 是否只用于传递给 React.memo 子组件？
- [ ] 是否避免了过度优化？
- [ ] 依赖数组是否正确？

## 自定义 Hooks
- [ ] 是否提取了可复用的逻辑？
- [ ] 返回值是否稳定？（使用 useCallback/useMemo）
- [ ] 是否处理了组件卸载后的状态更新？
- [ ] 是否有完整的 TypeScript 类型？

## 性能
- [ ] 是否避免了不必要的重渲染？
- [ ] 大型列表是否使用了虚拟化？
- [ ] 是否避免了在渲染中执行昂贵计算？
- [ ] 是否有合理使用 useRef 存储可变值？
