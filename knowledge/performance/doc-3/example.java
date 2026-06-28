```java
// 缓存策略示例：多级缓存
public class MultiLevelCache<K, V> {
    private final Cache<K, V> l1Cache;  // Caffeine（本地缓存）
    private final Cache<K, V> l2Cache;  // Redis（分布式缓存）
    
    public V get(K key) {
        // L1 缓存查询
        V value = l1Cache.getIfPresent(key);
        if (value != null) {
            return value;
        }
        // L2 缓存查询
        value = l2Cache.getIfPresent(key);
        if (value != null) {
            l1Cache.put(key, value);  // 回填 L1
            return value;
        }
        // 数据库查询（缓存穿透防护）
        value = loadFromDB(key);
        if (value != null) {
            l1Cache.put(key, value);
            l2Cache.put(key, value);
        } else {
            // 缓存空值，防止缓存穿透
            l1Cache.put(key, nullValue);
            l2Cache.put(key, nullValue, 30_000);  // 短过期
        }
        return value;
    }
}
```