# Kotlin 协程细则

## 强制规则 (MUST)

### 1. 使用 viewModelScope / lifecycleScope

```kotlin
// ✅ 正确：ViewModel 中使用 viewModelScope
class UserViewModel : ViewModel() {
    fun load() {
        viewModelScope.launch {
            val user = repository.getUser()
            _state.value = user
        }
    }
}

// ❌ 错误：GlobalScope 生命周期和组件不一致
GlobalScope.launch {  // ❌ 不会随 ViewModel 销毁取消
    val user = repository.getUser()
}
```

### 2. 正确的 Dispatcher 选择

```kotlin
// ✅ 正确：按操作类型选择 Dispatcher
suspend fun loadUser(id: Long): User = withContext(Dispatchers.IO) {
    api.getUser(id)  // IO 操作
}

suspend fun processData(data: Data): Result = withContext(Dispatchers.Default) {
    computeHeavy(data)  // CPU 密集
}

// Main 操作不需要切换
fun updateUI(user: User) {
    _name.text = user.name  // Main 线程
}

// ❌ 错误：在主线程执行网络请求
suspend fun loadUser(id: Long): User {
    return api.getUser(id)  // ❌ 网络请求在主线程
}
```

### 3. 异常处理用 try-catch 或 CoroutineExceptionHandler

```kotlin
// ✅ 正确：launch 内部 try-catch
viewModelScope.launch {
    try {
        val user = repository.getUser()
        _state.value = user
    } catch (e: Exception) {
        _error.value = "加载失败: ${e.message}"
    }
}

// ✅ 正确：全局异常处理器
val handler = CoroutineExceptionHandler { _, throwable ->
    Log.e("Coroutine", "未捕获异常", throwable)
}

viewModelScope.launch(handler) {
    // ...
}

// ❌ 错误：async 中异常不处理
val deferred = scope.async {
    throw RuntimeException()  // ❌ 异常被静默吞掉，直到 .await() 才抛出
}
```

### 4. 使用 Flow 处理数据流

```kotlin
// ✅ 正确：Flow 处理持续数据流
class UserRepository {
    fun getUsers(): Flow<List<User>> = flow {
        val users = api.getUsers()
        emit(users)
    }.flowOn(Dispatchers.IO)
}

// ❌ 错误：用 Channel 代替 Flow（Channel 是热数据流）
```

## 推荐实践 (SHOULD)

### 并行请求使用 async

```kotlin
viewModelScope.launch {
    val userDef = async { repository.getUser(id) }
    val postsDef = async { repository.getPosts(id) }
    val (user, posts) = userDef.await() to postsDef.await()
}
```

## 禁止行为 (MUST NOT)

- ❌ 使用 `GlobalScope`
- ❌ 在主线程执行 IO/CPU 操作
- ❌ 协程中不处理异常
- ❌ 使用 `runBlocking` 在 UI 线程
- ❌ 在非协程上下文中调用 suspend 函数
