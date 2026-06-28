# React 状态管理 Checklist

## 状态分层
- [ ] 组件局部状态是否使用 useState/useReducer？
- [ ] 全局状态是否适合放入 store（非表单、非临时）？
- [ ] 服务端数据是否使用 TanStack Query？
- [ ] 是否避免状态提升过度？

## Zustand
- [ ] 是否使用了 selector 避免全量渲染？
- [ ] store 是否按功能模块拆分？
- [ ] 是否避免将服务端数据放入 Zustand？
- [ ] 异步操作是否在 store action 中处理？

## Context
- [ ] 是否仅用于低频更新？
- [ ] 是否避免多层 Provider 嵌套？
- [ ] 是否提供了默认值？

## useReducer
- [ ] 复杂状态是否使用 useReducer？
- [ ] action 类型是否定义清晰？
- [ ] reducer 是否为纯函数？

## TanStack Query
- [ ] 缓存配置是否合理（staleTime/gcTime）？
- [ ] 是否处理了 loading/error 状态？
- [ ] mutation 后是否 invalidate 相关 query？
