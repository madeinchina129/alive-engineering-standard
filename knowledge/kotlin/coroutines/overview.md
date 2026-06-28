# Kotlin 协程规范

## 协程基础

Kotlin 协程是轻量级并发框架，通过 `suspend` 函数和 `CoroutineScope` 管理异步任务：

```kotlin
// suspend 函数：可挂起的函数
suspend fun fetchUser(id: Long): User {
    return withContext(Dispatchers.IO) {
        api.getUser(id)  // 网络请求
    }
}

// 在 ViewModel 中启动协程
class UserViewModel : ViewModel() {
    fun loadUser(id: Long) {
        viewModelScope.launch {
            val user = fetchUser(id)
            _user.value = user
        }
    }
}
```

---

## 协程构建器

| 构建器 | 返回值 | 用途 |
|--------|--------|------|
| `launch` | Job | 启动即忘，不返回结果 |
| `async` | Deferred | 返回结果，使用 `.await()` |
| `runBlocking` | T | 阻塞线程（仅测试/main） |

---

```kotlin
// launch：执行并忘记
scope.launch {
    saveToDatabase(data)
}

// async：获取结果
val deferred = scope.async { fetchData() }
val result = deferred.await()
```

---

## 适用范围

- **网络请求**：必须用协程管理
- **数据库操作**：Room 支持 suspend 查询
- **并行任务**：async/await 组合
- **定时任务**：delay 替代 Thread.sleep
