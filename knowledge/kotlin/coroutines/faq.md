# Kotlin 协程 FAQ

## Q: `launch` 和 `async` 的区别？

```
launch：不返回结果，返回 Job
async：返回结果，返回 Deferred<T>，需要 .await()
```

```kotlin
scope.launch { saveToDb() }  // 不关心结果
val result = scope.async { fetchData() }.await()  // 需要结果
```

## Q: `Dispatchers.Main`、`IO`、`Default` 的区别？

```
Main   → UI 线程（更新界面、LiveData 赋值）
IO     → 网络请求、文件读写、数据库
Default → CPU 密集计算（排序、解析）
```

## Q: `viewModelScope` 和 `lifecycleScope` 的区别？

```
viewModelScope → ViewModel 销毁时取消
lifecycleScope → LifecycleOwner 销毁时取消（Activity/Fragment）
```

```kotlin
// Fragment 中使用
lifecycleScope.launch {
    // 随 Fragment 生命周期
}
```

## Q: Flow 和 LiveData 怎么选？

```
LiveData：有生命周期感知，适合 UI 状态
Flow：更灵活，支持各种操作符，适合数据层
```

```kotlin
// 数据层用 Flow
class UserRepo {
    fun getUsers(): Flow<List<User>> = flow { ... }
}

// UI 层将 Flow 转为 LiveData
val users: LiveData<List<User>> = repo.getUsers().asLiveData()
```

## Q: 如何取消协程？

```kotlin
val job = scope.launch {
    repeat(100) {
        if (!isActive) return@launch  // 检查取消状态
        processItem(it)
    }
}
job.cancel()  // 取消
job.join()    // 等待取消完成
```

## Q: `withContext` 和 `async` 的区别？

```kotlin
// withContext：切换 Dispatcher，等待结果
val data = withContext(Dispatchers.IO) { fetch() }

// async：启动并行任务
val data = async(Dispatchers.IO) { fetch() }.await()
// 语义上 withContext 更适合切换线程
```
