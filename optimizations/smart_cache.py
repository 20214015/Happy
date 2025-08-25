"""
🚀 SMART CACHING SYSTEM  
Cache ADB commands và API calls để tăng tốc đáng kể
"""

import time
import json
import hashlib
from typing import Any, Optional, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

class CacheStrategy(Enum):
    """Chiến lược cache khác nhau"""
    IMMEDIATE = "immediate"      # Cache ngay lập tức
    LAZY = "lazy"               # Cache khi cần
    AGGRESSIVE = "aggressive"    # Cache mọi thứ
    SMART = "smart"             # Cache thông minh

@dataclass
class CacheEntry:
    """Entry trong cache với metadata"""
    data: Any
    timestamp: float
    access_count: int
    ttl: float  # Time to live
    size_bytes: int
    cache_key: str
    
    @property
    def is_expired(self) -> bool:
        return time.time() > (self.timestamp + self.ttl)
    
    @property 
    def age(self) -> float:
        return time.time() - self.timestamp

class SmartCache:
    """Smart caching system cho ADB commands"""
    
    def __init__(self, max_size_mb: int = 50, strategy: CacheStrategy = CacheStrategy.SMART):
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.strategy = strategy
        self.cache: Dict[str, CacheEntry] = {}
        self.hit_count = 0
        self.miss_count = 0
        
        # TTL defaults for different command types
        self.ttl_map = {
            'adb_devices': 5.0,           # Device list changes rarely
            'instance_list': 3.0,         # Instances change moderately  
            'app_list': 30.0,             # Apps change slowly
            'system_info': 60.0,          # System info very stable
            'file_operations': 1.0,       # File ops change quickly
        }
    
    def _generate_key(self, command: str, params: Dict = None) -> str:
        """Generate unique cache key"""
        key_data = {'cmd': command, 'params': params or {}}
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _estimate_size(self, data: Any) -> int:
        """Estimate memory size of data"""
        try:
            return len(json.dumps(data, default=str).encode())
        except:
            return len(str(data).encode())
    
    def _evict_if_needed(self, required_size: int):
        """LRU eviction khi cache đầy"""
        current_size = sum(entry.size_bytes for entry in self.cache.values())
        
        if current_size + required_size <= self.max_size_bytes:
            return
            
        # Sort by access frequency and age
        entries_by_priority = sorted(
            self.cache.items(),
            key=lambda x: (x[1].access_count, -x[1].age)
        )
        
        for key, entry in entries_by_priority:
            del self.cache[key]
            current_size -= entry.size_bytes
            if current_size + required_size <= self.max_size_bytes:
                break
    
    def get(self, command: str, params: Dict = None, command_type: str = 'default') -> Optional[Any]:
        """Get from cache"""
        cache_key = self._generate_key(command, params)
        
        if cache_key not in self.cache:
            self.miss_count += 1
            return None
            
        entry = self.cache[cache_key]
        
        # Check expiration
        if entry.is_expired:
            del self.cache[cache_key]
            self.miss_count += 1
            return None
            
        # Update access stats
        entry.access_count += 1
        self.hit_count += 1
        
        return entry.data
    
    def set(self, command: str, data: Any, command_type: str = 'default', params: Dict = None):
        """Set cache entry"""
        cache_key = self._generate_key(command, params)
        data_size = self._estimate_size(data)
        
        # Evict if needed
        self._evict_if_needed(data_size)
        
        # Determine TTL
        ttl = self.ttl_map.get(command_type, 10.0)
        
        # Smart TTL adjustment based on command type and data size
        if self.strategy == CacheStrategy.SMART:
            if data_size > 1024 * 100:  # Large data gets longer TTL
                ttl *= 2
            if command_type in ['system_info', 'app_list']:
                ttl *= 3  # Stable data gets longer TTL
        
        entry = CacheEntry(
            data=data,
            timestamp=time.time(),
            access_count=1,
            ttl=ttl,
            size_bytes=data_size,
            cache_key=cache_key
        )
        
        self.cache[cache_key] = entry
    
    def invalidate_pattern(self, pattern: str):
        """Invalidate cache entries matching pattern"""
        to_remove = [
            key for key in self.cache.keys() 
            if pattern in key
        ]
        for key in to_remove:
            del self.cache[key]
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        
        total_size = sum(entry.size_bytes for entry in self.cache.values())
        
        return {
            'hit_rate': f"{hit_rate:.1f}%",
            'total_entries': len(self.cache),
            'total_size_mb': f"{total_size / 1024 / 1024:.2f}",
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
        }

# Global cache instance
global_smart_cache = SmartCache()
